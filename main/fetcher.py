import requests
import json
import time
import datetime
from urllib.parse import quote, unquote

class Fetcher:
	def __init__(self, api_key):
		self.APIKey = api_key

	## Get account details by providing the account name
	def requestSummonerData(self, summoner_name):
		URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(quote(summoner_name), self.APIKey)
		response = requests.get(URL)
		return response.json()

	## Get an account's ranked match data by account ID
	def requestRankedData(self, account_ID):
		URL = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key={}".format(account_ID, self.APIKey)
		response = requests.get(URL)
		return response.json()
		
	## Get an account's ranked match history
	def requestMatchHistory(self, account_ID, queue_type=420, num_matches=1):
		URL = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?api_key={}&queue={}&endIndex={}".format(account_ID, self.APIKey, queue_type, num_matches)
		
		response = requests.get(URL)
		return response.json()

	def requestMatchDetails(self, match_ID):
		URL = "https://na1.api.riotgames.com/lol/match/v4/matches/{}?api_key={}".format(match_ID, self.APIKey)
		response = requests.get(URL)
		return response.json()
