import csv
import hashlib
import io
from contextlib import closing
from datetime import datetime

from django.db import connection

from app.models import Album, Artist, Genre


# TODO: a séparer en :viewmanager, playlist action, import action

## @package app.dao
# package containing the manual operations on the database

## Import a group of albums into the database in bulk mode
#   @param album the set of albums existing in the tracks to import
#   @param artists the artists existing in the set to import
#   @param totalTrack dict associating album title and track numbers
#   @param totalDisc dict associating album title and disc numbers
#   @return A dict containing the album title associated with the album id
def addAlbumBulk(albums, artists, totalTrack, totalDisc):
    albumReference = {"": Album.objects.get(title=None)}
    newAlbums = {}
    albumSet = set()

    # Transforming the dict into a set for the query
    for album in albums:
        albumSet.add(album)

    # Get all the existing artists in the table from our set
    albumInBase = Album.objects.filter(title__in=albumSet)
    albumToAdd = len(albumSet) - len(albumInBase)

    # Get the sequence value
    cursor = connection.cursor()
    cursor.execute("SELECT nextval('app_album_id_seq')")
    firstId = cursor.fetchone()
    # Offset the sequence value
    cursor.execute('ALTER SEQUENCE app_album_id_seq RESTART WITH {0};'.format(str(firstId[0] + albumToAdd)))

    # Add the known artists to the dict and remove the artist in the set
    for album in albumInBase:
        albumReference[album.title] = album.id
        del albums[album.title]

    # Creating the csv
    counter = 0
    virtualFile = io.StringIO()
    writer = csv.writer(virtualFile, delimiter='\t')
    for album in albums:
        newAlbums[album] = firstId[0] + counter
        writer.writerow([firstId[0] + counter, album, totalTrack[album], totalDisc[album]])
        counter += 1

    virtualFile.seek(0)
    # Import the csv into the database
    with closing(connection.cursor()) as cursor:
        cursor.copy_from(
            file=virtualFile,
            table='"app_album"',
            sep='\t',
            columns=('id', 'title', '"totalTrack"', '"totalDisc"'),
        )

    # Creating the csv for the link between artist and album
    virtualFile = io.StringIO()
    writer = csv.writer(virtualFile, delimiter='\t')
    for album in newAlbums:
        artistsAdded = albums[album].split(",")
        for artist in artistsAdded:
            writer.writerow([newAlbums[album], artists[artist]])

    virtualFile.seek(0)
    # Import the csv into the database
    with closing(connection.cursor()) as cursor:
        cursor.copy_from(
            file=virtualFile,
            table='"app_album_artist"',
            sep='\t',
            columns=('album_id', 'artist_id'),
        )
    virtualFile.close()

    return {**albumReference, **newAlbums}


## Import track into the database in bulk mode.
#   @param tracks the tracks objects.
#   @param artists the artist dict association the names and the ids.
#   @param albums the album dict association the albums title and the ids.
#   @param genres the genre associated with their ids.
#   @param playlistId the id of the playlist the track are added to.
def addTrackBulk(tracks, artists, albums, genres, playlistId):
    referenceTracks = {}

    # Moving the sequence before insert
    cursor = connection.cursor()
    cursor.execute("SELECT nextval('app_track_id_seq')")
    firstId = cursor.fetchone()
    # Offset the sequence value
    cursor.execute('ALTER SEQUENCE app_track_id_seq RESTART WITH {0};'.format(str(firstId[0] + len(tracks))))

    # Creating the csv
    counter = firstId[0]
    virtualFile = io.StringIO()
    writer = csv.writer(virtualFile, delimiter='\t')
    for track in tracks:
        writer.writerow([counter, track.location, track.title.replace('\n', '\\n').replace('\r', ''), track.year,
                         track.composer.replace('\n', '\\n').replace('\r', ''),
                         track.performer.replace('\n', '\\n').replace('\r', ''),
                         track.number, track.bpm, track.lyrics.replace('\n', "\\n").replace('\r', ''),
                         track.comment.replace('\n', '\\n').replace('\r', ''), track.bitRate, track.bitRateMode,
                         track.sampleRate, track.duration, track.discNumber, track.size, albums[track.album],
                         track.fileType, genres[track.genre],
                         track.coverLocation.replace('\n', '\\n').replace('\r', ''),
                         track.moodbar.replace('\n', '\\n').replace('\r', ''), track.scanned, track.playCounter,
                         datetime.now(), track.downloadCounter])
        referenceTracks[track] = counter
        counter += 1

    virtualFile.seek(0)
    # Import the csv into the database
    with closing(connection.cursor()) as cursor:
        cursor.copy_from(
            file=virtualFile,
            table='"app_track"',
            sep='\t',
            columns=('id', 'location', 'title', 'year', 'composer', 'performer', 'number', 'bpm', 'lyrics', 'comment',
                     '"bitRate"', '"bitRateMode"', '"sampleRate"', 'duration', '"discNumber"', 'size', 'album_id',
                     '"fileType_id"', 'genre_id', '"coverLocation"', 'moodbar', 'scanned', '"playCounter"',
                     '"lastModified"', '"downloadCounter"'),
        )

    # Creating the csv for the link between tracks and artists
    virtualFile = io.StringIO()
    writer = csv.writer(virtualFile, delimiter='\t')
    for track in tracks:
        for artist in track.artist:
            writer.writerow([referenceTracks[track], artists[artist]])

    virtualFile.seek(0)
    # Import the csv into the database
    with closing(connection.cursor()) as cursor:
        cursor.copy_from(
            file=virtualFile,
            table='"app_track_artist"',
            sep='\t',
            columns=('track_id', 'artist_id'),
        )

    # Creating csv for the link between tracks and playlist
    virtualFile = io.StringIO()
    writer = csv.writer(virtualFile, delimiter='\t')
    for track in tracks:
        writer.writerow([playlistId, referenceTracks[track]])

    virtualFile.seek(0)
    # Import the csv into the database
    with closing(connection.cursor()) as cursor:
        cursor.copy_from(
            file=virtualFile,
            table='"app_playlist_track"',
            sep='\t',
            columns=('playlist_id', 'track_id'),
        )
    virtualFile.close()


## Add new artists to the database in bulk mode
#   @param artists the set of the artists names
#   @return a dict associating the artists names with their ids
def addArtistBulk(artists):
    artistReference = {"": Artist.objects.get(name=None).id}
    newArtist = {}

    # Get all existing artist
    artistsInBase = Artist.objects.filter(name__in=artists)
    artistsToAdd = len(artists) - len(artistsInBase)

    # Get the sequence value
    cursor = connection.cursor()
    cursor.execute("SELECT nextval('app_artist_id_seq')")
    firstId = cursor.fetchone()
    # Offset the sequence value
    cursor.execute('ALTER SEQUENCE app_artist_id_seq RESTART WITH {0};'.format(str(firstId[0] + artistsToAdd)))

    # Add the known artists to the dict and remove the artist in the set
    for artist in artistsInBase:
        artistReference[artist.name] = artist.id
        artists.remove(artist.name)

    # Creating the structure for csv creation
    counter = 0
    for artist in artists:
        newArtist[artist] = firstId[0] + counter
        counter += 1

    # Creating the csv file from the information for DB import
    virtualFile = io.StringIO()
    writer = csv.writer(virtualFile, delimiter='\t')
    for artist in newArtist:
        writer.writerow([newArtist[artist], artist.rstrip()])

    virtualFile.seek(0)

    # Import the csv into the database
    with closing(connection.cursor()) as cursor:
        cursor.copy_from(
            file=virtualFile,
            table='"app_artist"',
            sep='\t',
            columns=('id', 'name'),
        )
    virtualFile.close()

    return {**artistReference, **newArtist}


## With a given set add the missing genre to the database and return a dict with name:id
#   @param genres the set of the genres to be added
#   @return A dict associating the genre name with their id
def addGenreBulk(genres):
    genreReference = {"": Genre.objects.get(name=None).id}
    newGenre = {}

    # Get all existing genre
    genreInBase = Genre.objects.filter(name__in=genres)
    genreToAdd = len(genres) - len(genreInBase)

    # Get the sequence value
    cursor = connection.cursor()
    cursor.execute("SELECT nextval('app_genre_id_seq')")
    firstId = cursor.fetchone()
    # Offset the sequence value
    cursor.execute('ALTER SEQUENCE app_genre_id_seq RESTART WITH {0};'.format(str(firstId[0] + genreToAdd)))

    # Add known genre into the dict and remove the genre known in database in the set
    for genre in genreInBase:
        genreReference[genre.name] = genre.id
        genres.remove(genre.name)

    # Creating the structure for DB import
    counter = 0
    for genre in genres:
        newGenre[genre] = firstId[0] + counter
        counter += 1

    # Creating a CSV file in memory for faster import in the database
    virtualFile = io.StringIO()
    writer = csv.writer(virtualFile, delimiter='\t')
    for genre in newGenre:
        writer.writerow([newGenre[genre], genre.rstrip()])

    virtualFile.seek(0)

    # Import the csv into the database
    with closing(connection.cursor()) as cursor:
        cursor.copy_from(
            file=virtualFile,
            table='app_genre',
            sep='\t',
            columns=('id', 'name'),
        )
    virtualFile.close()

    return {**genreReference, **newGenre}


##
def getViewName(playlist):
    return hashlib.md5(str(playlist.user.username).encode("ascii", "ignore") +
                       str(playlist.name).encode("ascii", "ignore") +
                       str(playlist.id).encode("ascii", "ignore")).hexdigest()


# Delete index and view after finished using it
def deleteView(playlist):
    viewName = getViewName(playlist)
    indexName = "index" + viewName
    sql = """DROP INDEX IF EXISTS "%s";""" % indexName
    with connection.cursor() as cursor:
        cursor.execute(sql)
    sql = """DROP MATERIALIZED VIEW IF EXISTS "%s" RESTRICT;""" % viewName
    with connection.cursor() as cursor:
        cursor.execute(sql)


# Creation of a view for each playlist with an index
def createViewForLazy(playlist):
    # Delete the old view if it exists
    deleteView(playlist)
    # Creating the hash for the view name
    viewName = getViewName(playlist)
    sql = """
            CREATE MATERIALIZED VIEW "%s" (track_id, track_title, track_year, composer, performer, bit_rate, duration, 
            cover, artists_names, artists_ids, genre_name, album_id, album_title, track_moodbar) AS SELECT *, 
            row_number() OVER() AS local_id FROM ( SELECT track.id, track.title, year, composer, performer, "bitRate", 
            duration, "coverLocation", string_agg(artist.name,  ';' ORDER BY artist.name) concatArtName, 
              string_agg(artist.id::character varying,';' ORDER BY artist.name) concatArtId, alb.title, genre.name,
               track.album_id, track.moodbar FROM app_track track
                left join app_album alb on track.album_id = alb.id
                left join app_album_artist on alb.id = app_album_artist.album_id
                left join app_artist artist on app_album_artist.artist_id = artist.id
                left join app_genre genre on track.genre_id = genre.id
                left join app_playlist_track playlist on track.id = playlist.track_id
                where playlist.playlist_id = %s
              GROUP BY alb.title, alb.title, track.title, number, "bitRate", track.id, genre.name
              ORDER BY concatArtName, alb.title, number) as result;
        """ % (viewName, '%s')
    with connection.cursor() as cursor:
        cursor.execute(sql, [str(playlist.id)])
    sql = """
        CREATE INDEX "%s" ON "%s" (local_id);
        """ % ("index" + viewName, viewName)
    with connection.cursor() as cursor:
        cursor.execute(sql)
    # Set the refresh flag to false
    playlist.refreshView = False
    playlist.save()


## Parse the raw sql query and add it to the existing dict
def lazyJsonGenerator(row, data, albumPositionMap, artistPositionMap):
    artists = row[8]
    album = row[10]

    # If the artist isn't in the map, we create it
    if artists not in artistPositionMap:
        # Adding the new artist position to the map
        artistPosition = len(data)
        artistPositionMap[artists] = artistPosition
        # Inserting the artist json into the result
        data.append({
            'IDS': row[9],
            'NAME': row[8],
            'ALBUMS': [],
        })
    else:
        # Getting the artist position in the map
        artistPosition = artistPositionMap[artists]

    # If the album isn't in the album map
    if album not in albumPositionMap:
        # Adding the new album position to the map
        albumPosition = len(data[artistPosition]['ALBUMS'])
        albumPositionMap[album] = albumPosition
        # Inserting the new album into the result
        data[artistPosition]['ALBUMS'].append({
            'ID': row[12],
            'NAME': row[10],
            'TRACKS': [],
        })
    else:
        albumPosition = albumPositionMap[album]

    # Adding the track information
    data[artistPosition]['ALBUMS'][albumPosition]['TRACKS'].append({
        'ID': row[0],
        'TITLE': row[1],
        'YEAR': row[2],
        'COMPOSER': row[3],
        'PERFORMER': row[4],
        'BITRATE': row[5],
        'DURATION': row[6],
        'COVER': row[7],
        'GENRE': row[11],
        'MOODBAR': row[13],
    })


# Return a queryset of tracks from a view
def getPlaylistTracksFromView(playlist, limit, offset):
    viewName = getViewName(playlist)
    sql = """SELECT * FROM "%s" WHERE local_id > %s LIMIT %s;""" % (viewName, '%s', '%s')
    with connection.cursor() as cursor:
        cursor.execute(sql, (offset, limit))
        return cursor.fetchall()


# Delete the associations between all the given tracks and artists and recreate it
def updateTrackArtists(tracks, artists, tracksIds):
    # Deleting old artists associations
    # TODO : Check if this really works
    sql = '''
    DELETE FROM app_track_artist WHERE track_id IN (
    '''
    params = []
    params.extend(tracksIds)
    for id in tracksIds:
        sql += "%s, "
    sql = sql[:-2]
    sql += ");"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql, tracksIds)

    # Recreating the link between artists and tracks
    sql = '''
    INSERT INTO app_track_artist (track_id, artist_id) VALUES 
    '''
    params = []
    for i in range(len(tracks)):
        for trackArtist in tracks[i].artist:
            artistId = artists[trackArtist]
            params.extend([tracksIds[i], artistId])
            sql += "(%s, %s), "
    sql = sql[:-2]
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql, params)


# Inserting song that aren't present in the playlist
def updatePlaylist(trackIds, playlistId):
    # Deleting all the playlist track associations
    sql = '''
    DELETE FROM app_playlist_track WHERE playlist_id = %s;
    '''
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql, [playlistId])

    # Recreating the associations
    sql = '''
    INSERT INTO app_playlist_track (playlist_id, track_id) VALUES
    '''
    params = []
    for trackId in trackIds:
        sql += " (%s, %s),"
        params.extend([playlistId, trackId])
    sql = sql[:-1]
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql, params)


def refreshPlaylist(tracks, artists, albums, genres, playlistId):
    # Default SQL query
    print(len(tracks))
    # If there is no tracks skip this part
    if len(tracks) > 0:
        sql = '''
        INSERT INTO app_track (location, "coverLocation", title, "year", "composer", "performer", "number", bpm, lyrics,
                           comment, "bitRate", "bitRateMode", "sampleRate", duration, "discNumber", size, "lastModified",
                           moodbar, scanned, "playCounter", "downloadCounter", album_id, "fileType_id", genre_id)
        VALUES 
        '''

        # Generating parameters and the request
        params = []
        for track in tracks:
            sql += "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s), "
            params.extend([track.location, track.coverLocation, track.title, track.year, track.composer, track.performer,
                           track.number, track.bpm, track.lyrics, track.comment, track.bitRate, track.bitRateMode,
                           track.sampleRate, track.duration, track.discNumber, track.size, datetime.now(),
                           track.moodbar, True, track.playCounter, track.downloadCounter, albums[track.album],
                           track.fileType, genres[track.genre]])
        sql = sql[:-2]
        # Finishing the query
        sql += '''
         ON CONFLICT (location) DO UPDATE
        SET title = EXCLUDED.title, "coverLocation" = EXCLUDED."coverLocation", year = EXCLUDED.year,
          composer = EXCLUDED.composer, performer = EXCLUDED.performer, number = EXCLUDED.number, bpm = EXCLUDED.bpm,
          lyrics = EXCLUDED.lyrics, comment = EXCLUDED.comment, "bitRate" = EXCLUDED."bitRate",
          "bitRateMode" = EXCLUDED."bitRateMode", "sampleRate" = EXCLUDED."sampleRate", duration = EXCLUDED.duration,
          "discNumber" = EXCLUDED."discNumber", size = EXCLUDED.size, "lastModified" = EXCLUDED."lastModified",
          moodbar = EXCLUDED.moodbar, scanned = TRUE, album_id = EXCLUDED.album_id, "fileType_id" = EXCLUDED."fileType_id",
          genre_id = EXCLUDED.genre_id 
        RETURNING id;
        '''

        tracksIds = []
        with closing(connection.cursor()) as cursor:
            # Executing the query and saving all the id inserted
            cursor.execute(sql, params)
            for row in cursor.fetchall():
                tracksIds.append(row[0])

        updateTrackArtists(tracks, artists, tracksIds)
        updatePlaylist(tracksIds, playlistId)
