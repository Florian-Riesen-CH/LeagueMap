import time
import requests
import json

from Object.Match import *

API_KEYS = ['RGAPI-aa6932d1-9e5b-4af9-9b7c-cdbc5abbb1cb','RGAPI-a086aa60-b73e-4acb-9ded-c6c136700130','RGAPI-735b78eb-6be9-41fd-afe9-2bce951954e1']
API_INDEX = 0
API_JUMP = 2
def incrementApiIndex():
    global REQUEST_CPT
    global API_INDEX
    print('changing API key')
    API_INDEX += 1
    if API_INDEX == 3:
        API_INDEX = 0

def findUuidBySummonerName(SummonerName: str):
    url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{SummonerName}?api_key={API_KEYS[API_INDEX]}'
        
    response = requests.request("GET", url)
    data = json.loads(response.text)
    return data['puuid']

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
    except Exception as e:
        # Gérer toutes les autres exceptions
        print(f"Une erreur est survenue : {e}")
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
            matchList.append(match)
            nbGetMatch += 1
            i += 1 
        

    


