class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        
        # Store player information
        self.players = {}

        # Store total team score
        self.total_score = 0 

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

    def calculatePlayerScores(self, game_duration):
        for player_id, player in self.players.items():
            player.calculateMetrics(game_duration)

        #Rescale metrics
        for metric in self.metrics:
            self.rescalePlayerMetrics(self.metrics)

        # Calculate scores
        for player_id, player in self.players.items():
            player.calculateScore()
            self.total_score += player.score

        # Normalize scores
        for player_id, player in self.players.items():
            player.score = player.score/self.total_score

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

    def serialize(self):
        team_dict = {'players':{}}
        team_dict['team_id'] = self.team_id
        team_dict['total_score'] = self.total_score

        for player_id, player in self.players.items():
            team_dict['players'][player_id] = player.serialize()

        return team_dict
