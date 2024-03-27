from typing import List
class winLose:
    def __init__(self, win) :
        self.cptWin = 0
        self.cptLose = 0
        self.winrate = 0
        if win:
            self.cptWin = 1
        else:
            self.cptLose = 1
    # Méthode pour convertir l'objet en dictionnaire
    def to_dict(self):
        return {
            'cptWin': self.cptWin,
            'cptLose': self.cptLose,
            'winrate': self.winrate,
        }


class DataSet:
    def __init__(self):
        self.dataSetLines = {}

    def adddataSetLine(self, champion, oppositeChampion, win):
        if champion in self.dataSetLines:
            if oppositeChampion in self.dataSetLines[champion]:
                if win:
                    self.dataSetLines[champion][oppositeChampion].cptWin += 1
                else:
                    self.dataSetLines[champion][oppositeChampion].cptLose += 1
            else: 
                self.dataSetLines[champion][oppositeChampion] = winLose(win)
        else:
            self.dataSetLines[champion] = {}
            self.dataSetLines[champion][oppositeChampion] = winLose(win)
        self.dataSetLines[champion][oppositeChampion].winrate = self.calculer_winrate(self.dataSetLines[champion][oppositeChampion].cptWin, self.dataSetLines[champion][oppositeChampion].cptLose)

    def calculer_winrate(self, nb_victoires, nb_defaites):
        if nb_victoires + nb_defaites == 0:
            return 0  # Éviter la division par zéro si aucune partie n'a été jouée
        winrate = (nb_victoires / (nb_victoires + nb_defaites)) * 100
        return winrate

    def to_dict(self):
        result = {}
        for champion, matches in self.dataSetLines.items():
            result[champion] = {op_champ: wl_record.to_dict() for op_champ, wl_record in matches.items()}
        return result

