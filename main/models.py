from django.db import models

class Summoner(models.Model):
    summoner_name = models.CharField(max_length=30)


class Match(models.Model):
    summoners = models.ManyToManyField(Summoner)

    match_id = models.BigIntegerField()
    date = models.DateField()
    duration = models.DurationField()

class Team(models.Model): 
    # Every team belongs to a match
    match = models.ForeignKey(
        'Match',
        on_delete=models.CASCADE,
    )

    team_id = models.CharField(max_length=4)
    
class Player(models.Model):
    # Each player belongs to a team
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
    )

    player_id = models.IntegerField()
    summoner_name = models.CharField(max_length=30)
    champion_name = models.CharField(max_length=30)
    

    # Info
    kills_actual = models.IntegerField()
    deaths_actual = models.IntegerField()
    assists_actual = models.IntegerField()
    kda = models.CharField(max_length=10)

    # Factors
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    champ_damage = models.DecimalField(max_digits=10, decimal_places=2)
    turrets_killed = models.IntegerField()
    turret_damage = models.DecimalField(max_digits=10, decimal_places=2)
    objective_damage = models.DecimalField(max_digits=10, decimal_places=2)
    vision_score = models.IntegerField()
    gold_earned = models.IntegerField()
    damage_taken = models.DecimalField(max_digits=10, decimal_places=2)
    damage_mitigated = models.DecimalField(max_digits=10, decimal_places=2)
    CC_given = models.IntegerField()
    
    # Metrics
    carry = models.DecimalField(max_digits=10, decimal_places=2)
    tank = models.DecimalField(max_digits=10, decimal_places=2)
    objectives = models.DecimalField(max_digits=10, decimal_places=2)
    support = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Match Influence Score
    match_influence = models.DecimalField(max_digits=10, decimal_places=2)
