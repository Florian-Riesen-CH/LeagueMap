from GetData import *
from Object.dataSet import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
app = FastAPI()
#Liste des domaines autorisés, '*' signifie tout domaine
origins = [
    "http://localhost:4200",
    "*",
]

# Configuration du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Les origines autorisées
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"],  # Les méthodes autorisées
    allow_headers=["X-Requested-With", "Content-Type"],  # Les en-têtes autorisés
)

@app.get("/getDatas")
def getDatas(sumonnerName:str, nbgame:int):
    matchList: List[Match] = getMatchsInformation(sumonnerName, nbgame)
    dataset: DataSet = DataSet()
    for match in matchList:
        for opponent in match.team_Opponent:
            dataset.adddataSetLine(match.championName, opponent.championName, match.win)
    json_data_method1 = json.dumps(dataset.to_dict())
    print(json_data_method1)
    return dataset


#vicorn main:app --reload
#getDatas('Flodel11',5)
