from scope.adn.get_usernames import *
from scope.crunchyroll.get_usernames import *
from breachdirectory import *
from BDD.scripts.adn import *
from BDD.scripts.crunchyroll import *

######################### BOUTON GET PSEUDOS FROM CRUNCHYROLL #########################

#on spécifie a coté du boutton le nombre souhaité d'ids d'animes pour l'execution de la récupération
#1 appel récupère entre 1 et 100 pseudos

def button_get_pseudos_crunchyroll(limit_ids):
    token = get_access_token()
    anime_ids = get_lastest_anime_ids(token, limit_ids)
    get_pseudos_from_crunchyroll(anime_ids, token)
    #implémenter la suite de la logique avec breachdirectory

######################### BOUTON GET PSEUDOS FROM ADN #########################

#on spécifie a coté du boutton le nombre souhaité d'appel serveur pour l'execution de la récupération
#1 appel récupère entre 1 et infini
    
def button_get_pseudos_adn(limit_call):
    starting_id = get_starting_id()
    get_username_from_adn(starting_id, limit_call)
    #implémenter la suite de la logique avec breachdirectory