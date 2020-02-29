import math
import json

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

        self.score = 0

        # Set summoner name
        self.summoner_name = None

    def calculateMetrics(self, game_duration): 
        self.metrics['carry'] = (( (1.5*self.factors['kills']+0.5*self.factors['assists']) ) * (self.factors['champ_damage'])) / (2 + 4 * (self.factors['deaths']))
        self.metrics['tank'] = (self.factors['damage_taken'] * self.factors['damage_mitigated']) / (2 + 2*(self.factors['deaths']))
        self.metrics['objectives'] = math.log(game_duration, 15)*(self.factors['turret_damage'] + self.factors['turrets_killed'] + self.factors['objective_damage'])
        self.metrics['support'] = (math.pow(self.factors['CC_given'], 2) + math.pow(self.factors['vision_score'],2.85) + 0.5*self.factors["kills"] + 1.5*self.factors["assists"])/ (2 + 3 * (self.factors['deaths']))
        
    def calculateScore(self):
        self.score = 0
        metric_scores = []
        self.score += math.pow(1+self.metrics['carry'], 3)
        self.score += math.pow(1+self.metrics['tank'], 2)
        self.score += math.pow(1+self.metrics['objectives'], 1.5)
        self.score += math.pow(1+self.metrics['support'], 1.75)
        # for metric_id, metric_score in self.metrics.items():
        #     self.score += math.pow(0.5+metric_score,3)

        self.score = math.pow(self.score, 1.25)

    def serialize(self):
        with open('main/assets/id_to_champ.txt') as json_file:
            id_to_champ = json.load(json_file)

        player_dict = {}
        player_dict["player_id"] = self.player_id
        player_dict["summoner_name"] = self.summoner_name
        player_dict["champion_name"] = id_to_champ[str(self.info['champion_id'])]
        player_dict["kills_actual"] = self.info['kills']
        player_dict["deaths_actual"] = self.info['deaths']
        player_dict["assists_actual"] = self.info['assists']
        player_dict["kda"] = self.info['kda']
        
        for factor in self.factors:
            player_dict[factor] = round(self.factors[factor]*100, 3)

        for metric in self.metrics:
            player_dict[metric] = round(self.metrics[metric]*100, 3)
        
        player_dict['score'] = round(self.score*100, 3)

        return player_dict
