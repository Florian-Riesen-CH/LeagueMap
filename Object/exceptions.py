class SummonerNameError(Exception):
    """Exception levée pour les erreurs liées au nom du summoner."""
    def __init__(self, summonerName, message="Nom du summoner introuvable ou erreur liée au summoner"):
        self.summonerName = summonerName
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} --> {self.summonerName}'