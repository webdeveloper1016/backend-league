from django.db import models

# Create your models here.
class SeasonFilter(models.Model):
    season = models.CharField(max_length=10)
    dataindex = models.IntegerField()
    data = models.TextField()

class SeasonWin(models.Model):
    dataindex = models.IntegerField()
    club = models.TextField()
    win = models.IntegerField()
    season = models.CharField(max_length=10)

class SeasonGoal(models.Model):
    dataindex = models.IntegerField()
    club = models.TextField()
    goal = models.IntegerField()
    season = models.CharField(max_length=10)

class SeasonShots(models.Model):
    dataindex = models.IntegerField()
    club = models.TextField()
    shots = models.IntegerField()
    season = models.CharField(max_length=10)