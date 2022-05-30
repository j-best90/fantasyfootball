from django.db import models
import uuid

class SquadsDataModel(models.Model):
    UUID = models.UUIDField(default=uuid.uuid4,primary_key=True)
    gameweek = models.CharField(max_length=250,blank=True,null=True)
    nameSquad = models.CharField(max_length=250,blank=True,null=True)
    element = models.CharField(max_length=250,blank=True,null=True)
    totalPoints = models.IntegerField(blank=True,null=True)
    minutes = models.IntegerField(blank=True,null=True)
    goals = models.IntegerField(blank=True,null=True)
    assists = models.IntegerField(blank=True,null=True)
    cleanSheets = models.IntegerField(blank=True,null=True)
    goalsConceded = models.IntegerField(blank=True,null=True)
    ownGoals = models.IntegerField(blank=True,null=True)
    penaltiesSaved = models.IntegerField(blank=True,null=True)
    penaltiesMissed = models.IntegerField(blank=True,null=True)
    yellowCards = models.IntegerField(blank=True,null=True)
    redCards = models.IntegerField(blank=True,null=True)
    saves = models.IntegerField(blank=True,null=True)
    bonus = models.IntegerField(blank=True,null=True)
    bps = models.IntegerField(blank=True,null=True)
    influence = models.FloatField(blank=True,null=True)
    creativity = models.FloatField(blank=True,null=True)
    threat = models.FloatField(blank=True,null=True)
    ict_index = models.FloatField(blank=True,null=True)
    values = models.IntegerField(blank=True,null=True)
    selected = models.IntegerField(blank=True,null=True)
    transfersIn = models.IntegerField(blank=True,null=True)
    transfersOut = models.IntegerField(blank=True,null=True)
    captain = models.BooleanField(default=False)
    viceCaptain = models.BooleanField(default=False)
    multiplier = models.IntegerField(blank=True,null=True)
    entryName = models.CharField(max_length=250,blank=True,null=True)
    eventTotal = models.IntegerField(blank=True,null=True)
    rank = models.IntegerField(blank=True,null=True)
    twentyTenName = models.CharField(max_length=250,blank=True,null=True)
    entry = models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        uniqueid = str(self.twentyTenName + self.gameweek)
        return uniqueid