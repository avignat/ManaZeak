from django.db import models
from django.db.models import DO_NOTHING

from app.models import MoodAverage, TrackInScopeStats


## This class is describing the table fileType.
class FileType(models.Model):
    ## The name of the file type (mp3, flac...).
    name = models.CharField(max_length=1000)


## The object representing an extracted cover
class Cover(models.Model):
    ## The path of the cover
    location = models.URLField(max_length=1000, null=True)


## The producer of a track or an album.
class Producer(models.Model):
    name = models.CharField(max_length=1000, unique=True, null=True)
    ## The description of the album
    description = models.CharField(max_length=1000, null=True)
    ## The cover location
    picture = models.URLField(max_length=1000, null=True)

    #       STATS
    ## Stat of the producer
    stat = models.ForeignKey(TrackInScopeStats, on_delete=DO_NOTHING, null=True)


## This class is describing the table genre.
class Genre(models.Model):
    ## The genre name
    name = models.CharField(max_length=1000, unique=True, null=True)
    ## The description of the album
    description = models.CharField(max_length=1000, null=True)
    ## The cover location
    picture = models.URLField(max_length=1000, null=True)

    #       STATS
    ## Stat of the genre
    stat = models.ForeignKey(TrackInScopeStats, on_delete=DO_NOTHING, null=True)


## This class is describing the table artists.
class Artist(models.Model):
    #           FOLDER INFORMATION
    ## The path of the artist folder.
    location = models.FilePathField(max_length=1000, unique=True, null=True)
    ## The name of the artist.
    folderName = models.CharField(max_length=1000, unique=True, null=True)
    ## The size of the folder.
    folderSize = models.IntegerField(null=True)

    #           METADATA
    ## The cover location
    picture = models.URLField(max_length=1000, null=True)
    ## The name of the artist.
    name = models.CharField(max_length=1000, unique=True, null=True)
    ## The real name of the artist.
    realName = models.CharField(max_length=1000, null=True)
    ## The description of the album
    description = models.CharField(max_length=1000, null=True)
    ## The genre linked to the track.
    genres = models.ManyToManyField(Genre)

    #       STATS
    ## Stat of the artist
    stat = models.ForeignKey(TrackInScopeStats, on_delete=DO_NOTHING, null=True)


## This class is describing the table album.
class Album(models.Model):
    #           FOLDER INFORMATION
    ## The path of the album folder.
    location = models.FilePathField(max_length=1000, unique=True)
    ## The folder name
    folderName = models.CharField(max_length=250)
    ## The size of the album folder.
    folderSize = models.IntegerField(null=True)
    ## The cover location
    cover = models.ForeignKey(Cover, on_delete=DO_NOTHING, null=True)
    #           METADATA
    ## The title of the album.
    title = models.CharField(max_length=1000, null=True)
    ## The description of the album
    description = models.CharField(max_length=1000, null=True)
    ## The producer of the album
    producer = models.ForeignKey(Producer, on_delete=DO_NOTHING, null=True)
    ## The album release artist
    releaseArtist = models.ForeignKey(Artist, on_delete=DO_NOTHING, related_name='album_release_artist', null=True)
    ## The year of the album release.
    year = models.IntegerField(null=True)

    #           STATS
    ## Stat of the genre
    stat = models.ForeignKey(TrackInScopeStats, on_delete=DO_NOTHING, null=True)


## This class is describing the table of track.
#   This table is the main table of the app it contains all the tracks of the app.
class Track(models.Model):
    #           FILE INFORMATION
    ## The path of the track.
    location = models.FilePathField(max_length=1000, unique=True)
    ## The file name
    fileName = models.CharField(max_length=250)
    ## The size of the track.
    fileSize = models.IntegerField()
    ## The file type linked to the track.
    fileType = models.ForeignKey(FileType, on_delete=models.CASCADE)
    ## The path of the cover.
    cover = models.ForeignKey(Cover, on_delete=DO_NOTHING)
    ## The track moodbar path.
    mood = models.URLField(max_length=1000, null=True)
    ## The duration of the track.
    duration = models.FloatField()
    ## The bit rate of the track.
    bitRate = models.IntegerField(null=True)
    ## The bit rate mode of the track (CBR, VBR).
    bitRateMode = models.IntegerField(null=True)
    ## The sample rate of the track.
    sampleRate = models.IntegerField(null=True)
    ## The last time the track was modified.
    lastModified = models.DateField(auto_now=True, null=True)  # to be used for freshly added track

    #           EMBEDDED METADATA
    ## The title of the app.
    title = models.CharField(max_length=1000)
    ## The year of creation of the track (metadata).
    year = models.IntegerField(null=True)
    ## The lyrics of the track.
    lyrics = models.CharField(max_length=42000, null=True)
    ## The comment on the track.
    comment = models.CharField(max_length=10000, null=True)
    ## The position of the track inside the album.
    trackNumber = models.IntegerField(null=True)
    ## The number of track in the album
    trackTotal = models.IntegerField(null=True)
    ## The disc number the track is on.
    discNumber = models.IntegerField(null=True)
    ## The beats per minute of the track.
    bpm = models.IntegerField(null=True)
    ## The album linked to the track.
    album = models.ForeignKey(Album, null=True, on_delete=models.DO_NOTHING)
    ## The producer of the track
    producer = models.ForeignKey(Producer, on_delete=DO_NOTHING)
    ## The genre linked to the track.
    genres = models.ManyToManyField(Genre)
    ## The composers of the track.
    composers = models.ManyToManyField(Artist, related_name='composer_artists')
    ## The performer of the track.
    performers = models.ManyToManyField(Artist, related_name='performer_artists')
    ## The artists linked to the track.
    artists = models.ManyToManyField(Artist)

    #           METADATA NOT IN FILE
    ## The number of time the track has been played.
    playCounter = models.IntegerField(default=0)
    ## The number of time the track has been downloaded.
    downloadCounter = models.IntegerField(default=0)
    ## The average value of the mood file
    moodAverage = models.ForeignKey(MoodAverage, on_delete=DO_NOTHING)

    #           FLAG
    ## If the track has been scanned by the rescan.
    scanned = models.BooleanField(default=False)
    ## A hash for linking the imported tracks to the tracks to import FIXME: voir si avec ça ou non
    # importHash = models.IntegerField()