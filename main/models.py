from django.db import models

class Match(models.Model):
    match_id = models.IntegerField(max_length=30)
    date = models.DateField()
    duration = models.DurationField()

class Team(models.Model): 
    team_id = models.CharField(max_length=4)
     
