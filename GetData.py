import time
import requests
import json

from Object.Match import *
from Object.exceptions import SummonerNameError

API_KEYS = ['RGAPI-2ec8176c-5fda-47b0-9103-cad7a73319f7']
API_INDEX = 0
API_JUMP = 40
def incrementApiIndex():
    global REQUEST_CPT
    global API_INDEX
    print('changing API key')
    API_INDEX += 1
    if API_INDEX == 1:
        API_INDEX = 0
    print(API_KEYS[API_INDEX])

def findUuidBySummonerName(SummonerName: str):
    url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{SummonerName}?api_key={API_KEYS[API_INDEX]}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['puuid']
    else:
        # Lever une SummonerNameError plutôt qu'une Exception générique
        raise SummonerNameError(SummonerName, f"Erreur HTTP {response.status_code} lors de la récupération du summoner.")

def getMatchHistoryByPuuid(Puuid:str, idFrom: int, count: int):
    if count > 100:
        count = 100
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{Puuid}/ids?start={idFrom}&count={count}&api_key={API_KEYS[API_INDEX]}'
    response = requests.request("GET", url)
    data = json.loads(response.text)
    return data

def getMatchInfoByMatchId(puuid:str, matchId:int):
    try:
        url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={API_KEYS[API_INDEX]}'
        response = requests.request("GET", url)
        data = json.loads(response.text)
        gameMode = data['info']['gameMode']
    except Exception as e:
        # Gérer toutes les autres exceptions
        print(f"Une erreur est survenue : {e}")
    if gameMode != 'CLASSIC':
        return None
    participants = data['info']['participants']
    teams = data['info']['teams']
    teamId = 0
    championId = 0
    championName = 0
    win:bool
    for participant in participants:
        if participant['puuid'] == puuid:
            teamId = participant['teamId']
            championId = participant['championId']
            championName = participant['championName']
            break
    for team in teams:
        if team['teamId'] == teamId:
            win = team['win']
            break
    
    match:Match = Match(data['info']['gameId'], data['info']['gameEndTimestamp'],championId,championName, win)
    for participant in participants:
        if participant['puuid'] != puuid:
            if participant['teamId'] == teamId:
                match.addMatchPlayerTeamAlly(MatchPlayer(participant['puuid'],participant['riotIdGameName'],participant['championId'],participant['championName'], participant['teamId']))
            else:
                match.addMatchPlayerTeamOpponent(MatchPlayer(participant['puuid'],participant['riotIdGameName'],participant['championId'],participant['championName'], participant['teamId']))
    return match

def getMatchsInformation(summonerName, nbMatch):
    nbGetMatch = 0
    matchList: List[Match] = []
    i = 0
    while i < nbMatch:
        if i % API_JUMP == 0:
            incrementApiIndex()
            myPuuid = findUuidBySummonerName(summonerName)
            myLastMatch = getMatchHistoryByPuuid(myPuuid, i, API_JUMP)
        for index, match in enumerate(myLastMatch):
            if nbGetMatch == nbMatch:
                return matchList
            print(f'{i} - Request for match: {match} ({API_KEYS[API_INDEX]})')
            match = getMatchInfoByMatchId(myPuuid, match)
            if match != None:
                matchList.append(match)
                nbGetMatch += 1
            i += 1 
    return matchList
        

    


