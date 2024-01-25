from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='wikimusic-welcome'),
    path('login/', views.logIn, name='wikimusic-login'),
    path('logout/', views.logOut, name='wikimusic-logout'),
    path('createaccount/', views.createAccount, name='wikimusic-createaccount'),
    path('list_artist/', views.listArtist, {'purpose': 'list'}, name='wikimusic-l-artist'),
    path('list_artist/album/', views.listArtist, {'purpose': 'album'}, name='wikimusic-l-artist-album'),
    path('list_artist/concert/', views.listArtist, {'purpose': 'concert'}, name='wikimusic-l-artist-concert'), 
    path('list_album/', views.listAlbum, {'purpose': 'list'}, name='wikimusic-l-album'),
    path('list_album/song/', views.listAlbum, {'purpose': 'song'}, name='wikimusic-l-album-song'),
    path('list_song/', views.listSong, name='wikimusic-l-song'),
    path('list_concert/', views.listConcert, name='wikimusic-l-concert'),
    path('register/artist', views.regArtist, name='wikimusic-r-artist'),
    path('register/album/<str:idArtist>/', views.regAlbum, name='wikimusic-r-album'),
    path('register/song/<int:idAlbum>/<int:idArtist>/', views.regSong, name='wikimusic-r-song'),
    path('register/concert/<str:idArtist>/', views.regConcert, name='wikimusic-r-concert'),
    path('visualize/artist/<str:idArtist>/', views.vArtist, name='wikimusic-v-artist'),
    path('visualize/album/<str:idAlbum>/', views.vAlbum, name='wikimusic-v-album'),
    path('visualize/song/<str:idSong>/', views.vSong, name='wikimusic-v-song'),
    path('visualize/concert/<str:idConcert>/', views.vConcert, name='wikimusic-v-concert'),
    
]
