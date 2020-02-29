from django.http import HttpResponse

from django.shortcuts import render

from django.template import loader

from urllib.parse import quote, unquote
from main.fetcher import Fetcher
from main.match import Match
import sys

APIKey = 'RGAPI-348fb156-b305-45b1-9c03-fee4763b1d30'

def verify(request):
    f = open('main/riot.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")

def search(request):
    return render(request, 'search.html')

def matchDetails(request, match_id):
    return render(request, 'search.html')

def summonerSummary(request, summoner_name, num_matches=20):
    fetcher = Fetcher(APIKey)

    # Request summoner data
    summoner_data = fetcher.requestSummonerData(summoner_name)
    if 'accountId' not in summoner_data:
        return render(request, 'empty.html')

    # Get match history data
    raw_match_history = fetcher.requestMatchHistory(summoner_data['accountId'], num_matches=num_matches)

    # Parse match history data
    matches = {}
    match_order = []
    for match in raw_match_history['matches']:
        match_id = match['gameId']
        timestamp = match['timestamp']
        raw_match_data = fetcher.requestMatchDetails(match_id)
        new_match = Match(match_id, raw_match_data, timestamp)

        matches[match_id] = new_match
        match_order.append(match_id)

        new_match.runCalculations()

    summoner_data = {'matches': {}}

    summoner_data['num_matches'] = num_matches
    for match_id, match in matches.items():
        summoner_data['matches'][match_id] = match.serialize()

    return render(request, 'summary.html', summoner_data)


