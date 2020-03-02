from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from urllib.parse import quote, unquote
from main.fetcher import Fetcher
from main.match import Match
import sys

from main.models import Match_model
from main.models import Team_model
from main.models import Player_model

APIKey = 'RGAPI-972d9b2d-544b-4eca-ad4f-ed2a6d459fb1'

def verify(request):
    f = open('main/static.riot.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")

def search(request):
    return render(request, 'search.html')

def matchDetails(request, match_id):
    return render(request, 'search.html')

def matchHistory(request, summoner_name, num_matches=20):
    fetcher = Fetcher(APIKey)

    # Request summoner data
    summoner_data = fetcher.requestSummonerData(summoner_name)
    if 'accountId' not in summoner_data:
        return render(request, 'empty.html')

    # Get match history data
    raw_match_history = fetcher.requestMatchHistory(summoner_data['accountId'], num_matches=num_matches)

    # Parse match history data
    matches = {}
    for match in raw_match_history['matches']:
        match_id = match['gameId']
        timestamp = match['timestamp']
       
        try:
            match_info = Match_model.objects.get(match_id=match_id)
        except:
            raw_match_data = fetcher.requestMatchDetails(match_id)
            new_match = Match(match_id, raw_match_data, timestamp)
            new_match.runCalculations()
            new_match.save_entry()

            match_info = Match_model.objects.get(match_id=match_id)

        red_info = Team_model.objects.filter(match=match, team_id='Red')
        blue_info = Team_model.objects.filter(match=match, team_id='Blue')

        red_players = Player_model.objects.filter(team=red_info)
        blue_players = Player_model.objects.filter(team=blue_info)

        matches[match_id] = {'match_info': match_info,
                             'teams': {'Red': { 'red_info': red_info,
                                                     'players': red_players
                                                   },
                                      'Blue': {'blue_info': blue_info,
                                                    'players': red_players
                                                   }
                                      }
                            }
    
    return render(request, 'summary.html', {'num_matches': num_matches, 'matches': matches})


# Code by Andrew Ho, Caltech 21'