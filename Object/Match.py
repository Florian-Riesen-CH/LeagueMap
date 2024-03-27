from typing import List
class MatchPlayer:
    def __init__(self, puuid: str, name: str, championId:int, championName:str, teamId:int):
        self.puuid = puuid
        self.name = name
        self.championId = championId
        self.championName = championName

class Match:
    def __init__(self, id: int, dateTimeStamp:int, championId:int, championName:str,win:bool):
        self.id = id
        self.dateTimeStamp = dateTimeStamp
        self.team_Ally: List[MatchPlayer] = []
        self.team_Opponent: List[MatchPlayer] = []
        self.championId = championId
        self.championName = championName
        self.win= win

    def addMatchPlayerTeamAlly(self, matchPlayer: MatchPlayer):
        self.team_Ally.append(matchPlayer)

    def addMatchPlayerTeamOpponent(self, matchPlayer: MatchPlayer):
        self.team_Opponent.append(matchPlayer)