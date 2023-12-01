import requests
from datetime import datetime, timedelta
import pandas as pd
import xml.etree.ElementTree as ET


# Définir les séries à importer avec leurs métadonnées
# 2020 = 100 Baseline par rapport à 2020
series_list = [
    {
        "symbol": "BBDP1",
        "key" : "M.DE.N.VPI.C.A00000.I20.A",
        "frequency": "M",
        "title": "Consumer Price Index",
        "description": "Overall Increase in Prices for a given basket of goods",
        "unit": "2020=100",
        "adjustments": "Unadjusted"
    },
    {
        "symbol": "BBDP1",
        "key":"A.DE.N.VPI.C.A00000.I20.A",
        "frequency": "A",
        "title": "Consumer Price Index",
        "description": "Overall Increase in Prices for a given basket of goods",
        "unit": "2020=100",
        "adjustments": "Unadjusted"
    },
    #...
]
# Fonction pour formater la date selon la fréquence
def format_date(timestamp, frequency):
    if frequency == 'M': # Mets la journée au 1er du mois
        return timestamp.replace(day=1)
    elif frequency == 'Q': # Mets le mois au 1er janvier avec 3 mois entre chaque observation 
        return timestamp.replace(month=1, day=1)
    elif frequency == 'A': # Mets le mois au 1er janvier avec 1 an entre chaque observartion
        return timestamp.replace(month=1, day=1)
    else:
        return timestamp

# Fonction pour faire un appel à l'API et formater les données
def fetch_and_format_data(symbol, key): 
    # Faire l'appel à l'API #mensuel api_url = "https://api.statistiken.bundesbank.de/rest/data/{flowRef}/{key}"
    #  Returns the time series from the specified dataflow (e.g. BBDY1) with the specified key (e.g. A.B10.N.G100.P0010.A).
    
    
    api_url = f"https://api.statistiken.bundesbank.de/rest/data/{symbol}/{key}"
        
    response = requests.get(api_url)

    # Fromstring pour utiliser directement le XML provenant de l'API, Parse pour utiliser un XML déjà enregistré sur le PC.
    root = ET.fromstring(response.text)
    
    # S'assurer que la data à bien été importée, voir le contenu
    if response.status_code == 200:
        print("La donnée à bien été importé")
        
    
    # Sinon print une erreur
    else:
         print(f"Erreur lors de la requête à l'API. Code d'état : {response.status_code}")

    # Formatée la data en fonction des critères voulus
    namespace = {'bbk': 'http://www.bundesbank.de/statistik/zeitreihen/BBKcompact'}

    # Récupérer la fréquence
    frequence = {
        'FREQ': root.find('.//bbk:Series', namespace).get('FREQ'),
    }

    # Récupérer les valeurs Time Period et Obs value
    value = {    
        'BBK_ID': root.find('.//bbk:Series', namespace).get('BBK_ID'),
        'OBS': [
         {'TIME_PERIOD': obs.get('TIME_PERIOD'), 'OBS_VALUE': obs.get('OBS_VALUE')}
            for obs in root.findall('.//bbk:Obs', namespace)
        ]
    }
    return frequence and value

    

data = fetch_and_format_data("BBDP1","M.DE.N.VPI.C.A00000.I20.A")


# Création d'un DataFrame Pandas
df = pd.DataFrame(data)

print(df)

        
    

