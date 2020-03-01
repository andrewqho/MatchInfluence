from main.player import Player
from main.team import Team

import json
import math
from datetime import datetime

from main.models import Match_model

class Match:
    def __init__(self, match_id, raw_match_data, timestamp):
        self.match_id = match_id
        self.date = datetime.fromtimestamp(timestamp/1000.0)

        # Get match data
        self.match_data = raw_match_data

        self.match_duration = self.match_data['gameDuration']/60

        self.teams = self.populateTeamsData()
        
    def getPlayerID(self, summoner_name):
        for player in self.match_data['participantIdentities']:
            if player['player']['summonerName'] == summoner_name:
                self.player_ID = player['participantId']

    def populateTeamsData(self):
        # Initialize new team_data structure
        teams = {'Blue': Team('Blue'), 
                     'Red': Team('Red')}

        # Parse team data
        for team_data in self.match_data["teams"]:
            team_id = 'Blue'
            if team_data["teamId"] == 200:
                team_id = 'Red'
            
            teams[team_id].info['win'] = False
            if team_data['win'] == 'Win':
                teams[team_id].info['win'] = True
            
            teams[team_id].bans = team_data["bans"]

            teams[team_id].info['dragons_killed'] = team_data['dragonKills']
            teams[team_id].info['barons_killed'] = team_data['baronKills']
            teams[team_id].info['heralds_killed'] = team_data['riftHeraldKills']

            teams[team_id].info['towers_killed'] = team_data['towerKills']
            teams[team_id].info['inhibs_killed'] = team_data['inhibitorKills']

        # Parse player data
        for player_data in self.match_data['participants']:
            # Create new player
            new_player_id = player_data['stats']['participantId']
            new_player = Player(new_player_id)
            
            new_player.info['champion_id'] = player_data['championId']
            new_player.info['spell1'] = player_data['spell1Id']
            new_player.info['spell2'] = player_data['spell2Id']
            new_player.info['lane'] = player_data['timeline']['lane']
            
            new_player.info['kills'] = player_data['stats']['kills']
            new_player.info['deaths'] = player_data['stats']['deaths']
            new_player.info['assists'] = player_data['stats']['assists']
            new_player.info['kda'] = 'Perfect'
            if player_data['stats']['deaths'] != 0:
                new_player.info['kda'] = (player_data['stats']['kills'] + player_data['stats']['assists'])/player_data['stats']['deaths']     
                new_player.info['kda'] = round(new_player.info['kda'], 2)

            new_player.factors['kills'] = player_data['stats']['kills']
            new_player.factors['deaths'] = player_data['stats']['deaths']
            new_player.factors['assists'] = player_data['stats']['assists']
            
            new_player.factors['champ_damage'] = player_data['stats']['totalDamageDealtToChampions']
            new_player.factors['turrets_killed'] = player_data['stats']['turretKills']
            new_player.factors['turret_damage'] = player_data['stats']['damageDealtToTurrets']
            new_player.factors['objective_damage'] = player_data['stats']['damageDealtToObjectives']
            new_player.factors['vision_score'] = player_data['stats']['wardsPlaced'] + 2*player_data['stats']['wardsKilled'] + 2*player_data['stats']['visionWardsBoughtInGame']
            new_player.factors['gold_earned'] = player_data['stats']['goldEarned']
            new_player.factors['damage_taken'] = player_data['stats']['totalDamageTaken']
            new_player.factors['damage_mitigated'] = player_data['stats']['damageSelfMitigated']     
            new_player.factors['CC_given'] = player_data['stats']['timeCCingOthers']
            
            if new_player_id < 6:
                teams['Blue'].players[new_player_id] = new_player
            else:
                teams['Red'].players[new_player_id] = new_player
        
        for player_data in self.match_data['participantIdentities']:
            playerID = player_data['participantId']
            new_player_name = player_data['player']['summonerName']
            
            team_id = 'Red'
            if playerID < 6:
                team_id = 'Blue'

            teams[team_id].setPlayerName(playerID, new_player_name)

        return teams

    def runCalculations(self):
        # Calculate scores
        for team_id, team in self.teams.items():
            team.calculatePlayerScores(self.game_duration)

    def save_entry(self):
        match_entry = Match_model(
            match_id=self.match_id,
            match_date=self.date,
            match_duration=self.match_duration
            )

        match_entry.save()

        self.teams['Blue'].save_entry(match_entry)
        self.teams['Red'].save_entry(match_entry)




# Code by Andrew Ho, Caltech 21'