## This class is a copy of a Track object. This object has less impact in memory.
from app.src.dto.album.localAlbum import LocalAlbum
from app.src.dto.artist.localArtist import LocalArtist


class LocalTrack(object):

    ## Constructor
    def __init__(self):
        self.id = None
        ## The path of the track.
        self.location = ''
        ## The path of the cover.
        self.coverLocation = ''
        ## The title of the app.
        self.title = ''
        ## The year of creation of the track (metadata).
        self.year = 0
        ## The composers of the track.
        self.composers = []
        ## The performers of the track.
        self.performers = []
        ## The producer of the track
        self.producer = ''
        ## The position of the track inside the album.
        self.number = 0
        ## The beats per minute of the track.
        self.bpm = 0
        ## The lyrics of the track.
        self.lyrics = ''
        ## The comment on the track.
        self.comment = ''
        ## The bit rate of the track.
        self.bitRate = 0
        ## The bit rate mode of the track (CBR, VBR).
        self.bitRateMode = 0
        ## The sample rate of the track.
        self.sampleRate = 0
        ## The duration of the track.
        self.duration = 0
        ## The disc number the track is on.
        self.discNumber = 0
        ## The size of the track.
        self.size = 0
        ## The artists linked to the track.
        self.artists = []
        ## The album linked to the track.
        self.album = LocalAlbum()
        ## The genre linked to the track.
        self.genres = []
        ## The file type linked to the track.
        self.fileType = 0
        ## The track moodbar path.
        self.moodbar = ''
        ## If the track has been scanned by the rescan.
        self.scanned = False
        ## The number of time the track has been played.
        self.playCounter = 0
        ## The number of time the track has been downloaded.
        self.downloadCounter = 0
        ## The folder name of the artist containing the file
        self.artistFolderName = ''
        ## The name of the album artist
        self.albumArtist = LocalArtist()