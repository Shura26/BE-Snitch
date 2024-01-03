import os
import requests
from bdd_interaction import *


#Envoie la requete a l'API breachdirectory
def req_breach(pseudo):
    key = os.environ.get('API_BREACHDIRECTORY')
    url = f"https://BreachDirectory.com/api_usage?method=username&key={key}&query={pseudo}"
    response = requests.get(url)

    if response.ok:
        data = response.json()

        for entry in data:
            # Vérifier si les  champs email, username et domaine sont présent
            if 'domain' in entry and entry['domain'] and 'email' in entry and entry['email'] and 'username' in entry and entry['username']:
                domain = entry['domain']
                email = entry['email']
                username = entry['username']

                add_compromised_user(username, email, domain)

    else:
        print(f"Erreur : {response.text}")