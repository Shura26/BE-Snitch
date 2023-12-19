import cloudscraper, json, sys
from  BDD.scripts.adn import update_adn_starting_id

#itère sur toutes les commentaires d'animes d'adn grâce au bruteforce de tous les id d'animes, retourne chaque pseudo trouvé à partir du start_id (commence a 699)
def get_username_from_adn(start_id_anime, limit_server_call):

    current_id_anime = start_id_anime
    scraper = cloudscraper.create_scraper() 
    usernames = []

    for _ in range(limit_server_call):
        response = scraper.get(f"https://gw.api.animationdigitalnetwork.fr/comment/show/{current_id_anime}").text
        json_data = json.loads(response)

        for commentaire in json_data.get("comments", []):
            username = commentaire.get("user", {}).get("username", None)
            if username:
                usernames.append(username)

        current_id_anime += 1

    update_adn_starting_id(current_id_anime)

    return usernames
