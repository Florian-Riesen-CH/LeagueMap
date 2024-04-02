from GetData import *
from Object.dataSet import *
from fastapi import FastAPI, HTTPException
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
    try:
        matchList: List[Match] = getMatchsInformation(sumonnerName, nbgame)
    except SummonerNameError as e:
        # Vous pouvez retourner un statut d'erreur HTTP spécifique avec un message
        raise HTTPException(status_code=404, detail=f"Erreur : {e}")
    
    dataset: DataSet = DataSet()
    for match in matchList:
        for opponent in match.team_Opponent:
            dataset.adddataSetLine(match.championName, opponent.championName, match.win)
    json_data_method1 = json.dumps(dataset.to_dict())
    print(json_data_method1)
    return dataset


#vicorn main:app --reload
#getDatas('Flodel11',5)
#pip install requests && pip install fastapi && pip install uvicorn && export PATH=$PATH:/opt/render/.local/bin && uvicorn main:app --host 0.0.0.0 --port $PORT;