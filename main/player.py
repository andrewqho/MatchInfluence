import math
import json

from main.models import Player_model

class Player:
    def __init__(self, player_id):
        # Set player id
        self.player_id = player_id
        
        # Initialize player info
        self.info = {}

        # Initialize factors
        self.factors = {}

        # Initialize metrics
        self.metrics = {}

        self.match_influence = 0

        # Set summoner name
        self.summoner_name = None

    def calculateMetrics(self, game_duration): 
        self.metrics['carry'] = (( (1.5*self.factors['kills']+0.5*self.factors['assists']) ) * (self.factors['champ_damage'])) / (2 + 4 * (self.factors['deaths']))
        self.metrics['tank'] = (self.factors['damage_taken'] * self.factors['damage_mitigated']) / (2 + 2*(self.factors['deaths']))
        self.metrics['objectives'] = math.log(game_duration, 15)*(self.factors['turret_damage'] + self.factors['turrets_killed'] + self.factors['objective_damage'])
        self.metrics['support'] = (math.pow(self.factors['CC_given'], 2) + math.pow(self.factors['vision_score'],2.85) + 0.5*self.factors["kills"] + 1.5*self.factors["assists"])/ (2 + 3 * (self.factors['deaths']))
        
    def calculateScore(self):
        metric_scores = []
        self.match_influence += math.pow(1+self.metrics['carry'], 3)
        self.match_influence += math.pow(1+self.metrics['tank'], 2)
        self.match_influence += math.pow(1+self.metrics['objectives'], 1.5)
        self.match_influence += math.pow(1+self.metrics['support'], 1.75)
        # for metric_id, metric_score in self.metrics.items():
        #     self.score += math.pow(0.5+metric_score,3)

        self.match_influence = math.pow(self.match_influence, 1.25)

    def save_entry(self, team_obj):
        with open('main/assets/id_to_champ.txt') as json_file:
            id_to_champ = json.load(json_file)

        player_entry = Player_model(
            team=team_obj,
            player_id=self.player_id,
            summoner_name=self.summoner_name,
            champion_name=id_to_champ[str(self.info['champion_id'])],
            kills_actual=self.info['kills'],
            deaths_actual=self.info['deaths'],
            assists_actual=self.info['assists'],
            kda=self.info['kda'],
            kills=self.factors['kills'],
            deaths=self.factors['deaths'],
            assists=self.factors['assists'],
            champ_damage=self.factors['champ_damage'],
            turrets_killed=self.factors['turrets_killed'],
            turret_damage=self.factors['turret_damage'],
            objective_damage=self.factors['objective_damage'],
            vision_score=self.factors['vision_score'],
            gold_earned=self.factors['gold_earned'],
            damage_taken=self.factors['damage_taken'],
            damage_mitigated=self.factors['damage_mitigated'],
            CC_given=self.factors['CC_given'],
            carry=round(self.metrics['carry']*100, 3),
            tank=round(self.metrics['tank']*100, 3),
            objectives=round(self.metrics['objectives']*100, 3),
            support=round(self.metrics['support']*100, 3),
            match_influence=round(self.match_influence*100, 3)
        )

        player_entry.save()


# Code by Andrew Ho, Caltech 21'