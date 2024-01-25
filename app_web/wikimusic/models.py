from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]


class Artist (models.Model):
    idArtist = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    born = models.DateTimeField()
    death = models.DateTimeField(null=True, blank=True)
    bornCountry = models.CharField(max_length=30)
    bornCity = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self) -> str:
        return super().__str__() + self.firstname + ', ' + self.surname

class Album (models.Model):
    idAlbum = models.IntegerField(primary_key=True)
    albumName = models.CharField(max_length=40)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    release = models.DateTimeField()
    lengthAlbum = models.CharField(max_length=5, validators=[RegexValidator(regex=r'^\d{2}:\d{2}$', message='Invalid time format. Use mm:ss format.')])
    numSongs = models.PositiveSmallIntegerField()
    urlAlbum = models.URLField()

    def __str__(self) -> str:
        return super().__str__() + self.albumName + ' - ' + self.artist.firstname + self.artist.surname

class Song (models.Model):
    idSong = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    albumSong = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    artistsSong = models.ManyToManyField(Artist)
    lengthSong = models.CharField(max_length=5, validators=[RegexValidator(regex=r'^\d{2}:\d{2}$', message='Invalid time format. Use mm:ss format.')])
    lyrics = models.TextField(blank=True, null=True)
    urlSong = models.URLField()

    def __str__(self) -> str:
        artists = ", ".join(str(artist) for artist in self.artistsSong.all())
        return f"{self.title} - {artists}"

class Concert(models.Model):
    idConcert = models.IntegerField(primary_key=True)
    concertName = models.CharField(max_length=100)
    artistConcert = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='concerts')
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self) -> str:
        return super().__str__() + self.concertName + ' - ' + self.artistConcert.firstname + ' ' + self.artistConcert.surname + ' - ' + self.location
