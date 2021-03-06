import logging
from crontab import CronTab
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.html import strip_tags

from app.achievement import refreshAchievements, checkAchievement
from app.errors.errors import ErrorEnum, errorCheckMessage
from app.models import FileType, Genre, Album, Artist, Permissions, Groups, UserPreferences, Playlist, TransactionType


## @package app.utils
# This package contains utility functions.


## Logger needed for writing into the log file.
from app.models.views import ViewType

logger = logging.getLogger('django')


## Split a table in x tables of equal size.
#   @param table the table that need to be split.
#   @param numberOfCluster the number of partition the table need to be split.
#   @return numberOfCluster tables that can be created from the size of the original table.
def splitTable(table, numberOfCluster):
    if len(table) % numberOfCluster == 0:
        chunkSize = int(len(table) / numberOfCluster)
    else:
        chunkSize = int(len(table) / numberOfCluster) + 1
    for i in range(0, len(table), chunkSize):
        yield table[i:i + chunkSize]


## Process a Vorbis tag to remove the useless info.
#   @param tag the vobis tag
#   @return the cleaned tag
def processVorbisTag(tag):
    tag = strip_tags(tag)
    tag = tag[2:]
    tag = tag[:-2]
    return tag


## Transform a timecode to a string readable for humans.
#   @param timestamp the timestamp object (date object in DB)
#   @return a string of the format "DD/MM/YYYY - HH:MM"
def timeCodeToString(timestamp):
    return str(timestamp.day).zfill(2) + "/" + str(timestamp.month).zfill(2) + \
           "/" + str(timestamp.year) + " - " + str(timestamp.hour) + ":" + \
           str(timestamp.minute)


## Check if a user has the given permission.
#   @param requirements the permission required.
#   @param user the user asking for permission.
#   @return True if the user has permission, False otherwise.
def checkPermission(requirements, user):
    checkAchievement(user)
    userPref = UserPreferences.objects.get(user=user)
    permissions = userPref.group.permissions
    if permissions.filter(code__in=requirements).count() == len(requirements):
        return True
    else:
        return False


## Set a flag in the database asking for regenerating all the postgres views
def refreshAllViews():
    for playlist in Playlist.objects.all():
        if not playlist.refreshView:
            playlist.refreshView = True
            playlist.save()


## Create the default entries into the database.
#   Generate in database :
#   - the file types
#   - the default artist
#   - the default album
#   - the default genre
#   - the permissions
#   - the transaction types
#   - the default groups
#   Creating the cron jobs and refresh the achievement of the base from the data stored in the enum
def populateDB():
    if FileType.objects.all().count() == 0:
        print("Created files types")
        FileType(name="mp3").save()
        FileType(name="ogg").save()
        FileType(name="flac").save()
        FileType(name="wav").save()
    if Artist.objects.all().count() == 0:
        print("Created default artist")
        Artist(name=None).save()
    if Album.objects.all().count() == 0:
        print("Created default album")
        Album(title=None).save()
    if Genre.objects.all().count() == 0:
        print("Created default genre")
        Genre(name=None).save()
    if Permissions.objects.all().count() == 0:
        print("Creating default permissions")
        Permissions(name="Login", code="LOGI").save()
        Permissions(name="Music listening", code="PLAY").save()
        Permissions(name="Playlist management", code="PLST").save()
        Permissions(name="Download", code="DOWN").save()
        Permissions(name="Wish creation", code="WISH").save()
        Permissions(name="Tag submission", code="TAGS").save()
        Permissions(name="Upload file", code='UPLD').save()
        Permissions(name="Sponsor right", code='SPON').save()
        Permissions(name="Stats access", code='STAT').save()
        Permissions(name="Child stats access", code="STCH").save()
        Permissions(name="Family stat access", code="STFA").save()
        Permissions(name="Wish review", code="WISR").save()
        Permissions(name="Access to library stats", code="STAL").save()
        Permissions(name="Change genre description", code="DESC").save()
        Permissions(name="Tag edition", code="TAGE").save()
        Permissions(name="Upload aproval", code="UPAP").save()
        Permissions(name="All stats", code="STAA").save()
        Permissions(name="Access to adminView", code="ADMV").save()
        Permissions(name="Edit user group", code="GRPE").save()
        Permissions(name="Access to whole family tree", code="FTAL").save()
        Permissions(name="Library management", code="LIBR").save()
        Permissions(name="Grant admin privileges", code="GAPR").save()
        Permissions(name="Coin gift", code="COIN").save()

    if TransactionType.objects.all().count() == 0:
        print("Creating default transaction types")
        TransactionType(name="Listening", code="PLAY", coinGain=100, coinLoss=0, streakGain=0, streakLoss=0,
                        bubbles=False).save()
        TransactionType(name="Edit tag", code="TAGE", coinGain=100, coinLoss=300, streakGain=2, streakLoss=10,
                        bubbles=True).save()
        TransactionType(name="Upload", code="UPLD", coinGain=300, coinLoss=100, streakGain=5, streakLoss=6,
                        bubbles=True).save()
        TransactionType(name="Wish", code="WISH", coinGain=50, coinLoss=20, streakGain=1, streakLoss=10,
                        bubbles=True).save()
        TransactionType(name="Gift", code="GIFT", coinGain=1, coinLoss=0, streakGain=0, streakLoss=0,
                        bubbles=False).save()
        TransactionType(name="Bubble", code="BUBL", coinGain=0, coinLoss=0, streakGain=0, streakLoss=0,
                        bubbles=False).save()
    if Groups.objects.all().count() == 0:
        Groups(name="Banned", rank=0).save()
        print("Creating the defaults groups")
        Groups(name="Naab", rank=1).save()
        Groups(name="User", rank=2).save()
        Groups(name="Moderator", rank=3).save()
        Groups(name="Admin", rank=4).save()
        Groups(name="Root", rank=5).save()
        for group in Groups.objects.all():
            fillDefaultPermission(group)

    if ViewType.objects.all().count() == 0:
        ViewType(name="LIST").save()
        ViewType(name="ALBUM").save()
    # Creating and updating achivements
    setCronJobs()
    refreshAchievements()


## Add the permission to a group given the user rank
#   @param group the Group object of a user
def fillDefaultPermission(group):
    if group.rank > 0:
        group.permissions.add(Permissions.objects.get(code="LOGI"))
        group.permissions.add(Permissions.objects.get(code="PLAY"))
        group.permissions.add(Permissions.objects.get(code="PLST"))
        group.permissions.add(Permissions.objects.get(code="DOWN"))
    if group.rank > 1:
        group.permissions.add(Permissions.objects.get(code="WISH"))
        group.permissions.add(Permissions.objects.get(code="TAGS"))
        group.permissions.add(Permissions.objects.get(code="UPLD"))
        group.permissions.add(Permissions.objects.get(code="SPON"))
        group.permissions.add(Permissions.objects.get(code="STAT"))
    if group.rank > 2:
        group.permissions.add(Permissions.objects.get(code="STCH"))
        group.permissions.add(Permissions.objects.get(code="STFA"))
        group.permissions.add(Permissions.objects.get(code="WISR"))
        group.permissions.add(Permissions.objects.get(code="STAL"))
    if group.rank > 3:
        group.permissions.add(Permissions.objects.get(code="DESC"))
        group.permissions.add(Permissions.objects.get(code="TAGE"))
        group.permissions.add(Permissions.objects.get(code="UPAP"))
        group.permissions.add(Permissions.objects.get(code="STAA"))
        group.permissions.add(Permissions.objects.get(code="ADMV"))
        group.permissions.add(Permissions.objects.get(code="GRPE"))
        group.permissions.add(Permissions.objects.get(code="FTAL"))
        group.permissions.add(Permissions.objects.get(code="LIBR"))
    if group.rank > 4:
        group.permissions.add(Permissions.objects.get(code="GAPR"))
        group.permissions.add(Permissions.objects.get(code="COIN"))


## Create the cron job if the job don't exists
def setCronJobs():
    cron = CronTab("root")
    # Checking the job already present
    if checkIfCronJobExists('rescan', cron):
        job = cron.new(command='python /ManaZeak/manage.py rescan', comment='rescan')
        job.hours.on(4)
        job.dow.on('MON')
        cron.write()


@login_required(redirect_field_name='login.html', login_url='app:login')
## Delete all the jobs in the crontab and create the cron tab from the function setCronJobs()
#   @param request the request from the navigator
def refreshCrontab(request):
    if request.method == 'GET':
        user = request.user
        if checkPermission(['LIBR'], user):
            cron = CronTab("root")
            for job in cron:
                cron.remove(job)
            setCronJobs()
            data = errorCheckMessage(True, None, refreshCrontab)
        else:
            data = errorCheckMessage(False, ErrorEnum.PERMISSION_ERROR, refreshCrontab, user)
    else:
        data = errorCheckMessage(False, ErrorEnum.BAD_REQUEST, refreshCrontab)
    return JsonResponse(data)


def checkIfCronJobExists(comment, cron):
    i = 0
    for _ in cron.find_comment(comment):
        i += 1
    return i == 0
