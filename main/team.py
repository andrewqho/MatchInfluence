from main.models import Team_model

class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        
        # Store player information
        self.players = {}

        # Store total team match influence
        self.total_match_influence = 0 

        # Store team information
        self.info = {}
        
        # Iterable player information
        self.factors = ['kills',
                        'deaths',
                        'assists',
                        'champ_damage',
                        'turrets_killed',
                        'turret_damage',
                        'objective_damage',
                        'vision_score',
                        'gold_earned',
                        'damage_taken',
                        'damage_mitigated',
                        'CC_given']

        self.metrics = ['carry',
                        'tank',
                        'objectives',
                        'support']
    
    def setPlayerName(self, player_id, summoner_name):
        self.players[player_id].summoner_name = summoner_name

    def calculatePlayerMatchInfluences(self, match_duration):
        for player_id, player in self.players.items():
            player.calculateMetrics(match_duration)

        #Rescale metrics
        for metric in self.metrics:
            self.rescalePlayerMetrics(self.metrics)

        # Calculate scores
        for player_id, player in self.players.items():
            player.calculateMatchInfluence()
            self.total_match_influence += player.match_influence

        # Normalize scores
        for player_id, player in self.players.items():
            player.match_influence = player.match_influence/self.total_match_influence

    def rescalePlayerFactors(self):
        for factor in self.factors:
            # Calculate factor total
            total = 0

            for player_id, player in self.players.items():
                total += player.factors[factor]

            if total:
                # Rescale factor for all players
                for player_id, player in self.players.items():
                    player.factors[factor] = player.factors[factor] / total

    def rescalePlayerMetrics(self, metric):
        for metric in self.metrics:
            # Calculate metric total
            total = 0

            for player_id, player in self.players.items():
                total += player.metrics[metric]

            if total:
                # Rescale factor for all players
                for player_id, player in self.players.items():
                    player.metrics[metric] = player.metrics[metric] / total

    def save_entry(self, match_obj):

        team_entry = Team_model(
            match=match_obj,
            team_id=self.team_id,
            total_match_influence=self.total_match_influence,
            win=self.info['win'],
            dragons_killed=self.info['dragons_killed'],
            barons_killed=self.info['dragons_killed'],
            heralds_killed=self.info['heralds_killed'],
            towers_killed=self.info['towers_killed'],
            inhibs_killed=self.info['inhibs_killed']
        )

        team_entry.save()

        for player_id, player in self.players:
            player.save_entry(team_entry)

# Code by Andrew Ho, Caltech 21'