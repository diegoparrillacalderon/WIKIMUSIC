from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ArtistForm(forms.Form):
    firstname = forms.CharField(label='Firstname', max_length=20)
    surname = forms.CharField(label='Surname', max_length=20)
    born = forms.DateTimeField(label='Date of birth', widget=forms.SelectDateWidget(years=range(1800, datetime.now().year)))
    death = forms.DateTimeField(label='Date of death', widget=forms.SelectDateWidget(years=range(1800, datetime.now().year + 1)), required=False)
    bornCountry = forms.CharField(label='Country of birth', max_length=30)
    bornCity = forms.CharField(label='City of birth', max_length=30)
    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

class AlbumForm(forms.Form):
    albumName = forms.CharField(label='Name', max_length=40)
    release = forms.DateTimeField(label='Release date', widget=forms.SelectDateWidget(years=range(1800, datetime.now().year + 1)))
    lengthAlbum = forms.CharField(label='Lenght of the album', max_length=5)
    numSongs = forms.IntegerField(label='Number of songs', min_value=1)
    urlAlbum = forms.URLField()

class SongForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    lengthSong = forms.CharField(label='Length of te song', max_length=5)
    lyrics = forms.CharField(label='Description', widget=forms.Textarea, required=False)
    urlSong = forms.URLField()
    additional_artists = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Additional Artists'
    )

class ConcertForm(forms.Form):
    concertName = forms.CharField(label='Name', max_length=100)
    location = forms.CharField(label='Location', max_length=100)
    date = forms.DateTimeField(label='Date', widget=forms.SelectDateWidget)
    time = forms.TimeField()

class LogInUsers(forms.Form):
    username = forms.CharField(label='User name', max_length=50, widget=forms.TextInput(attrs={'placeholder':'User name'}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))