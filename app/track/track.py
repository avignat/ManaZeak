import json
import zipfile

import os

import zlib
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.html import strip_tags

from app.errors.errors import ErrorEnum, errorCheckMessage
from app.history import addToHistory
from app.models import Track
from app.stats.stats import addToStats
from app.utils import checkPermission


## @package app.track.track
#   Manges the track object


from app.wallet import checkListeningGain


## Scan all the attributes of an MP3 track, and add it to base.
#   @param track a track object
def exportTrackInfo(track):
    if track.genre is not None:
        genre = track.genre.name
    else:
        genre = None

    artists = []
    for artist in track.artist.all():
        artists.append({
            'ID': artist.id,
            'NAME': artist.name,
        })

    album = {}
    if track.album is not None:
        albumArtists = []
        for artist in track.album.artist.all():
            albumArtists.append({
                'ID': artist.id,
                'NAME': artist.name,
            })
        album = {
            'ID': track.album.id,
            'TITLE': track.album.title,
            'TOTAL_DISC': track.album.totalDisc,
            'TOTAL_TRACK': track.album.totalTrack,
            'ARTISTS': albumArtists,
        }

    data = {
        'ID': track.id,
        'TITLE': track.title,
        'YEAR': track.year,
        'COMPOSER': track.composer,
        'PERFORMER': track.performer,
        'TRACK_NUMBER': track.number,
        'BPM': track.bpm,
        'LYRICS': track.lyrics,
        'COMMENT': track.comment,
        'BITRATE': track.bitRate,
        'SAMPLERATE': track.sampleRate,
        'DURATION': track.duration,
        'GENRE': genre,
        'FILE_TYPE': track.fileType.name,
        'DISC_NUMBER': track.discNumber,
        'SIZE': track.size,
        'LAST_MODIFIED': track.lastModified,
        'COVER': track.coverLocation,
        'ARTISTS': artists,
        'ALBUM': album,
        'PLAY_COUNTER': track.playCounter,
        'FILENAME': os.path.basename(track.location)
    }
    return data


@login_required(redirect_field_name='login.html', login_url='app:login')
## Get all the information about a track.
#   @param request a POST request containing :
#       - the track id to get the information (TRACK_ID)
#   @return a json response containing :
#       - the id of the track (ID)
#       - the title of the track (TITLE)
#       - the year of the track (YEAR)
#       - the composer of the track (COMPOSER)
#       - the performer (PERFORMER)
#       - the track number (TRACK_NUMBER)
#       - the track bpm (BPM)
#       - the track lyrics (LYRICS)
#       - the track comment (COMMENT)
#       - the track bitrate (BITRATE)
#       - the track samplerate (SAMPLERATE)
#       - the track duration (DURATION)
#       - the track genre (GENRE)
#       - the track file type (FILE_TYPE)
#       - the track disc number (DISC_NUMBER)
#       - the track size (SIZE)
#       - the track file last modified date (LAST_MODIFIED)
#       - the track cover path (COVER)
#       - a artist object containing :
#           -
def getTracksDetailedInfo(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        user = request.user
        if checkPermission(["PLAY"], user):
            if 'TRACK_ID' in response:
                trackIds = response['TRACK_ID']
                trackInfo = []
                for trackId in trackIds:
                    if Track.objects.filter(id=trackId).count() == 1:
                        trackInfo.append(exportTrackInfo(Track.objects.get(id=trackId)))
                    else:
                        data = errorCheckMessage(False, ErrorEnum.DB_ERROR, getTracksDetailedInfo)
                        return JsonResponse(data)
                data = {**dict({'RESULT': trackInfo}), **errorCheckMessage(True, None, getTracksDetailedInfo)}
            else:
                data = errorCheckMessage(False, ErrorEnum.BAD_FORMAT, getTracksDetailedInfo, user)
        else:
            data = errorCheckMessage(False, ErrorEnum.PERMISSION_ERROR, getTracksDetailedInfo, user)
    else:
        data = errorCheckMessage(False, ErrorEnum.BAD_REQUEST, getTracksDetailedInfo)
    return JsonResponse(data)


# Return the link to a track with a track id
@login_required(redirect_field_name='login.html', login_url='app:login')
def getTrackPath(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        user = request.user
        if checkPermission(["PLAY"], user):
            # Checking JSON keys
            if 'TRACK_ID' in response and 'PREVIOUS' in response and 'LAST_TRACK_PATH' in response \
                    and 'TRACK_PERCENTAGE' in response:
                trackId = strip_tags(response['TRACK_ID'])
                # Getting the track asked
                if Track.objects.filter(id=trackId).count() == 1:
                    track = Track.objects.get(id=trackId)
                    # If we don't ask a previous track
                    if not bool(response['PREVIOUS']):
                        # Adding the current track to the history
                        # Removing the first 2 chars
                        previousTrackPath = strip_tags(response['LAST_TRACK_PATH'])[2:]
                        # If the previous track exists
                        if Track.objects.filter(location=previousTrackPath).count() == 1:
                            listeningPercentage = float(strip_tags(response['TRACK_PERCENTAGE']))
                            previousTrack = Track.objects.get(location=previousTrackPath)
                            checkListeningGain(previousTrack, user)
                            # Adding to stats if the user has listened more than 15% of the song
                            if listeningPercentage > 5:
                                previousTrack.playCounter += 1
                                previousTrack.save()
                                addToStats(previousTrack, listeningPercentage, user)
                        addToHistory(track, user)

                    # Returning the asked song
                    data = {
                        'TRACK_PATH': track.location,
                    }
                    data = {**data, **errorCheckMessage(True, None, getTrackPath)}
                else:
                    data = errorCheckMessage(False, ErrorEnum.DB_ERROR, getTrackPath)
            else:
                data = errorCheckMessage(False, ErrorEnum.BAD_FORMAT, getTrackPath, user)
        else:
            data = errorCheckMessage(False, ErrorEnum.PERMISSION_ERROR, getTrackPath, user)
    else:
        data = errorCheckMessage(False, ErrorEnum.BAD_REQUEST, getTrackPath)
    return JsonResponse(data)


# Return the mood file with a given track id
@login_required(redirect_field_name='login.html', login_url='app:login')
def getMoodbar(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        user = request.user
        if checkPermission(["PLAY"], user):
            if 'TRACK_ID' in response:
                trackID = response['TRACK_ID']
                if Track.objects.filter(id=trackID).count() == 1:
                    track = Track.objects.get(id=trackID)
                    data = {
                        'TRACK_MOOD': track.moodbar,
                    }
                    data = {**data, **errorCheckMessage(True, None, getMoodbar)}
                else:
                    data = errorCheckMessage(False, ErrorEnum.DB_ERROR, getMoodbar)
            else:
                data = errorCheckMessage(False, ErrorEnum.BAD_FORMAT, getMoodbar, user)
        else:
            data = errorCheckMessage(False, ErrorEnum.PERMISSION_ERROR, getMoodbar, user)
    else:
        data = errorCheckMessage(False, ErrorEnum.BAD_REQUEST, getMoodbar)
    return JsonResponse(data)


# Download the given song
@login_required(redirect_field_name='login.html', login_url='app:login')
def getDownloadLocation(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        user = request.user
        if checkPermission(["DOWN"], user):
            if 'TRACK_ID' in response:
                trackId = strip_tags(response['TRACK_ID'])
                if Track.objects.filter(id=trackId).count() == 1:
                    track = Track.objects.get(id=trackId)
                    track.downloadCounter += 1
                    track.save()
                    data = {
                        'DOWNLOAD_PATH': track.location,
                    }
                    data = {**data, **errorCheckMessage(True, None, getDownloadLocation)}
                else:
                    data = errorCheckMessage(False, ErrorEnum.DB_ERROR, getDownloadLocation)
            else:
                data = errorCheckMessage(False, ErrorEnum.BAD_FORMAT, getDownloadLocation, user)
        else:
            data = errorCheckMessage(False, ErrorEnum.PERMISSION_ERROR, getDownloadLocation, user)
    else:
        data = errorCheckMessage(False, ErrorEnum.BAD_REQUEST, getDownloadLocation)
    return JsonResponse(data)


# Download a zip of different song
@login_required(redirect_field_name='login.html', login_url='app:login')
def multiTrackDownload(request):
    if request.method == "POST":
        response = json.loads(request.body)
        user = request.user
        if checkPermission(["DOWN"], user):
            if 'TRACKS_ID' in response:
                trackIds = response['TRACKS_ID']
                # TODO : create admin option max number of sound to download
                if len(trackIds) > 50:
                    return JsonResponse(errorCheckMessage(False, None, multiTrackDownload))
                locations = []

                # Getting tracks requested by the user
                for trackId in trackIds:
                    if Track.objects.filter(id=trackId).count() == 1:
                        track = Track.objects.get(id=trackId)
                        locations.append(track.location)
                tmp = ""
                for loc in locations:
                    tmp += loc
                archiveName = "ManaZeak-" + str(zlib.crc32(tmp.encode("ascii", "ignore"))) + ".zip"

                # Checking if the output folder for the zip exists
                if not os.path.isdir("/static/zip"):
                    try:
                        os.makedirs("/static/zip")
                    except OSError:
                        return JsonResponse(errorCheckMessage(False, ErrorEnum.DIR_CREATION_ERROR, multiTrackDownload))

                # Creating archive
                archiveName = os.path.join("/static/zip", archiveName)
                archive = zipfile.ZipFile(archiveName, 'w', zipfile.ZIP_DEFLATED)
                for location in locations:
                    archive.write(location, os.path.basename(location), compress_type=zipfile.ZIP_DEFLATED)

                data = {**{'DOWNLOAD_PATH': archiveName, }, **errorCheckMessage(True, None)}
            else:
                data = errorCheckMessage(False, ErrorEnum.BAD_FORMAT, multiTrackDownload)
        else:
            data = errorCheckMessage(False, ErrorEnum.PERMISSION_ERROR, multiTrackDownload, user)
    else:
        data = errorCheckMessage(False, ErrorEnum.BAD_REQUEST, multiTrackDownload)
    return JsonResponse(data)
