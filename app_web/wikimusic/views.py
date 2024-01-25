from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import ArtistForm, AlbumForm, SongForm, ConcertForm, LogInUsers, CustomUserCreationForm
from .models import Artist, Album, Song, Concert
from .templates import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from django.urls import reverse_lazy, reverse

# Create your views here.

# HOME PAGE     
def welcome(request):
    listArtist = Artist.objects.all()
    listAlbum = Album.objects.all()
    listSong = Song.objects.all()
    listConcert = Concert.objects.all()
    return render(request, WELCOME, {'listArtist': listArtist, 'listAlbum': listAlbum, 'listSong': listSong, 'listConcert': listConcert})

@login_required(login_url=reverse_lazy('wikimusic-login'))
def logOut(request):
    logout(request)
    return redirect ('wikimusic-welcome')

def logIn(request):
    if (request.method == 'POST'):
        form = LogInUsers(request.POST)
        if (form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if (user is not None):
                if (request.user.is_authenticated ):
                    logout(request)
                login(request, user)
                nextPage=request.GET.get('next')
                if ( nextPage is None ):
                    nextPage = reverse('wikimusic-welcome')
                return redirect (nextPage)
            else:
                error='Incorrect user name or password.'
                return render(request, LOGIN_USERS, {'form':form, 'errorMsg':error })
        else:
            error="Some form field data are incorrect."
            return render(request, LOGIN_USERS, {'form':form, 'errorMsg':error })
    else:
        form = LogInUsers()
        if ( request.GET.get('error403') is None):
            error=None
        else:
            error='Operation not allowed. Use an account with sufficient permissions'
        return render(request, LOGIN_USERS, {'form':form, 'errorMsg': error })


def createAccount(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('wikimusic-welcome')
    else:
        form = CustomUserCreationForm()
    
    return render(request, CREATE_ACCOUNT, {'form': form})


@login_required(login_url=reverse_lazy('wikimusic-login'))
def regArtist(request):
    if (request.method == 'POST'):
        form = ArtistForm(request.POST)
        if (form.is_valid()):
            firstname = form.cleaned_data['firstname']
            surname = form.cleaned_data['surname']
            born = form.cleaned_data['born']
            death = form.cleaned_data['death']
            bornCountry = form.cleaned_data['bornCountry']
            bornCity = form.cleaned_data['bornCity']
            gender = form.cleaned_data['gender']

            # Get the latest artist ID
            last_artist = Artist.objects.last()
            new_id = 1 if last_artist is None else last_artist.idArtist + 1

            newArtist = Artist(idArtist=new_id, firstname=firstname, surname=surname, born=born, death=death, bornCountry=bornCountry, bornCity=bornCity, gender=gender)
            try:
                newArtist.save()
                return redirect('wikimusic-welcome')
            except IntegrityError:
                error = "There is already an artist with this name and surname " + firstname + surname
                return render(request, REGISTER_ARTIST, {'form': form, 'errorMsg':error})
        else:
            error="The data in some form field is incorrect. Please check them."
            return render(request, REGISTER_ARTIST, {'form': form, 'errorMsg':error})
    else:
        form = ArtistForm()
    return render(request, REGISTER_ARTIST, {'form':form})


@login_required(login_url=reverse_lazy('wikimusic-login'))
def regAlbum(request, idArtist):
    artist = Artist.objects.get(idArtist=idArtist)
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            albumName = form.cleaned_data['albumName']
            release = form.cleaned_data['release']
            lengthAlbum = form.cleaned_data['lengthAlbum']
            numSongs = form.cleaned_data['numSongs']
            urlAlbum = form.cleaned_data['urlAlbum']

            # Get the latest album ID
            last_album = Album.objects.last()
            new_id = 1 if last_album is None else last_album.idAlbum + 1

            newAlbum = Album(idAlbum=new_id, albumName=albumName, release=release, lengthAlbum=lengthAlbum, numSongs=numSongs, urlAlbum=urlAlbum)
            try:
                newAlbum.artist=artist
                newAlbum.save()
                return redirect('wikimusic-welcome')
            except IntegrityError:
                error = "There is already an album of this artist with this name " + albumName
                return render(request, REGISTER_ALBUM, {'form': form, 'errorMsg':error})
        else:
            error="The data in some form field is incorrect. Please check them."
            return render(request, REGISTER_ALBUM, {'form': form, 'errorMsg':error})
    else:
        form = AlbumForm()
    return render(request, REGISTER_ALBUM, {'form':form, 'artist': artist})


@login_required(login_url=reverse_lazy('wikimusic-login'))
def regSong(request, idArtist, idAlbum):
    artist = Artist.objects.get(idArtist=idArtist)
    album = Album.objects.get(idAlbum=idAlbum)
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            lengthSong = form.cleaned_data['lengthSong']
            lyrics = form.cleaned_data['lyrics']
            urlSong = form.cleaned_data['urlSong']
            additional_artists = form.cleaned_data['additional_artists']

            # Get the latest song ID
            last_song = Song.objects.last()
            new_id = 1 if last_song is None else last_song.idSong + 1

            newSong = Song(idSong=new_id, title=title, lengthSong=lengthSong, lyrics=lyrics, urlSong=urlSong)
            try:
                newSong.albumSong=album
                newSong.save()
                newSong.artistsSong.add(*additional_artists)
                newSong.artistsSong.add(artist)
                
                return redirect('wikimusic-welcome')
            except IntegrityError:
                error = "There is already a song of this artist with this name " + title
                return render(request, REGISTER_SONG, {'form': form, 'errorMsg':error})
        else:
            error="The data in some form field is incorrect. Please check them."
            return render(request, REGISTER_SONG, {'form': form, 'errorMsg':error})
    else:
        form = SongForm()
    return render(request, REGISTER_SONG, {'form':form, 'artist':artist, 'album':album})

@login_required(login_url=reverse_lazy('wikimusic-login'))
def regConcert(request, idArtist):
    artist = Artist.objects.get(idArtist=idArtist)
    if request.method == 'POST':
        form = ConcertForm(request.POST)
        if form.is_valid():
            concertName = form.cleaned_data['concertName']
            location = form.cleaned_data['location']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']

            # Get the latest concert ID
            last_concert = Concert.objects.last()
            new_id = 1 if last_concert is None else last_concert.idConcert + 1

            newConcert = Concert(idConcert=new_id, concertName=concertName, location=location, date=date, time=time)
            try:
                newConcert.artistConcert=artist
                newConcert.save()
                return redirect('wikimusic-welcome')
            except IntegrityError:
                error = "There is already a concert of this artist with this name " + concertName
                return render(request, REGISTER_CONCERT, {'form': form, 'errorMsg':error})
        else:
            error="The data in some form field is incorrect. Please check them."
            return render(request, REGISTER_CONCERT, {'form': form, 'errorMsg':error})
    else:
        form = ConcertForm()
    return render(request, REGISTER_CONCERT, {'form':form, 'artist': artist})


def listArtist(request, purpose):
    list = Artist.objects.all()
    return render(request, LIST_ARTIST, {'list': list, 'purpose': purpose})

def listAlbum(request, purpose):
    listAlbum = Album.objects.all()
    listArtist = Artist.objects.all()
    return render(request, LIST_ALBUM, {'listAlbum':listAlbum, 'listArtist':listArtist, 'purpose': purpose})

def listSong(request):
    list = Song.objects.all()
    return render(request, LIST_SONG, {'list': list})

def listConcert(request):
    list = Concert.objects.all()
    return render(request, LIST_CONCERT, {'list': list})


def vArtist(request, idArtist):
    artist = Artist.objects.get(idArtist=idArtist)
    return render(request, VISUALIZE_ARTIST, {'artist': artist})

def vAlbum(request, idAlbum):
    album = Album.objects.get(idAlbum=idAlbum)
    return render(request, VISUALIZE_ALBUM, {'album': album})

def vSong(request, idSong):
    song = Song.objects.get(idSong=idSong)
    return render(request, VISUALIZE_SONG, {'song': song})

def vConcert(request, idConcert):
    concert = Concert.objects.get(idConcert=idConcert)
    return render(request, VISUALIZE_CONCERT, {'concert': concert})
