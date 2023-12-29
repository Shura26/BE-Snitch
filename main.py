import cloudscraper, json, requests
import smtplib, ssl
from email.message import EmailMessage

# obtient un token d'access auprès du serveur de crunchyroll pour pouvoir requeter le serveur plus tard
def get_access_token():
    data = {
        "grant_type": "client_id"
    }
    headers = {
        "Authorization": "Basic Y3Jfd2ViOg==",
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.post("https://www.crunchyroll.com/auth/v1/token", data=data, headers=headers).text
    json_data = json.loads(response)

    return json_data.get("access_token")


# récupère les 100 derniers id d'anime ajoutés
def get_lastest_anime_ids(token):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.get(
        f"https://www.crunchyroll.com/content/v2/discover/browse?n=10&sort_by=newly_added&ratings=true&locale=fr-FR",
        headers=headers).text
    json_data = json.loads(response)
    ids = []

    for item in json_data.get("data"):
        anime_id = item.get("id", None)

        if anime_id:
            ids.append(anime_id)

    with open("anime_ids.txt", "w") as ids_file:
        ids_file.write("\n".join(map(str, ids)))

    return ids



# récupère tous les usernames qui ont postés des commentaires sur un anime
def get_usernames_from_comments(id_anime, token):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    scraper = cloudscraper.create_scraper()
    page_size = 100
    usernames = []

    # Obtenez le nombre total de commentaires
    response = scraper.get(
        f"https://www.crunchyroll.com/content-reviews/v2/fr-FR/review/series/{id_anime}/list?page=1&page_size=100&sort=helpful",
        headers=headers).text
    json_data = json.loads(response)
    total_comments = json_data.get("total", 0)

    if total_comments > 100:
        # Obtenez tous les commentaires de manière itérative
        for page in range(1, (total_comments // page_size) + 2):
            response = scraper.get(
                f"https://www.crunchyroll.com/content-reviews/v2/fr-FR/review/series/{id_anime}/list?page={page}&page_size={page_size}&sort=helpful",
                headers=headers).text
            json_data = json.loads(response)

            # Extraire les noms d'utilisateur
            for item in json_data.get("items", []):
                username = item.get("author", {}).get("username", None)

                if username:
                    usernames.append(username)
    else:
        # Extraire les noms d'utilisateur
        for item in json_data.get("items", []):
            username = item.get("author", {}).get("username", None)

            if username:
                usernames.append(username)

    with open("usernames.txt", "a") as usernames_file:
        usernames_file.write("\n".join(usernames) + "\n")
    return usernames


def tri_usernames(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        lines = []
#set pour enlever les doublons
    unique_lines = list(set(lines))

    with open(file_path, "w") as file:
        file.write("\n".join(unique_lines) + "\n")


#pour tester sur 50 username
def extract_usernames(input_file, output_file, num_usernames=50):
    try:
        with open(input_file, "r") as input_file:
            lines = input_file.readlines()
    except FileNotFoundError:
        print(f"Le fichier {input_file} n'existe pas.")
        return

    # Extraire les 50 premiers usernames (ou moins si le fichier en contient moins)
    extracted_usernames = lines[:num_usernames]

    # Écrire les usernames extraits dans un autre fichier
    with open(output_file, "w") as output_file:
        output_file.write("".join(extracted_usernames))



def req_breach(pseudo, output_file):
    key = ""
    url = f"https://BreachDirectory.com/api_usage?method=username&key={key}&query={pseudo}"
    response = requests.get(url)

    if response.ok:
        data = response.json()

        with open(output_file, "a") as file:
            for entry in data:
                # Vérifier la présence et la non-nullité des champs nécessaires
                if 'domain' in entry and entry['domain'] and 'email' in entry and entry['email'] and 'username' in entry and entry['username']:
                    title = entry.get('title', 'N/A')
                    domain = entry['domain']
                    email = entry['email']
                    username = entry['username']
                    ip = entry.get('ip', 'N/A')

                    # Écrire dans le fichier uniquement si tous les champs sont présents et non vides
                    print(f"Title: {title}, Domain: {domain}, Email: {email}, Username: {username}, IP: {ip}", file=file)
    else:
        print(f"Erreur de requête : {response.status_code}")
        print(f"Message d'erreur : {response.text}")

def mail_sender() :
    #mail = "nakamaprotect@outlook.fr"
    password = ""


    with open("breach.txt", "r") as breachFile:
        #usernmaes=breachFile.read().splitlines()

        for username in breachFile:
            email_split = username.split("Email:")
            domain_split = username.split("Domain:")
            username_split = username.split("Username:")

            mail = email_split[1].strip().split(",")[0]
            domain = domain_split[1].strip().split(",")[0]
            username = username_split[1].strip().split(",")[0]

            msg = EmailMessage()
            msg.set_content(
                "Bonjour, nous sommes Nakamaprotect un projet visant à préserver la confidentialité de vos comptes sur internet."
                "\nNous avons découvert que des identifiants liés à l'identifiant " + username + " ont potentiellement fuité sur ce site : " + domain +
                "\nNous vous conseillons de ne plus utiliser le mots de passe utiliser sur ce site avec ce mail ou l'identifiant."
                "\nSi vous n'êtes pas concerné par ce mail nous nous excusons de la gêne occasionnée")
            msg["Subject"] = "Nakamaprotect"

            msg["From"] = "nakamaprotect@outlook.fr"
            msg["To"] = mail

            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.office365.com", port=587) as smtp:
                smtp.starttls(context=context)
                smtp.login(msg["From"], password)
                smtp.send_message(msg)





#token = get_access_token()
#anime_ids = get_lastest_anime_ids(token)

#for anime_id in anime_ids:
#    get_usernames_from_comments(anime_id, token)

#tri_usernames("usernames.txt")

#with open("usernames.txt", "r") as file:
#    nb_usernames= len(file.readlines())
#    print("Nombres de usernames: ",nb_usernames)

#extract_usernames("usernames.txt", "extracted_usernames.txt", num_usernames=50)


with open("extracted_usernames.txt", "r") as usernames_file:
    usernames = usernames_file.read().splitlines()

with open("breach.txt", "a") as output_file:
    for username in usernames:
        req_breach(username, "breach.txt")


#mail_sender()


#usernames_scraped = 0
#for anime_id in anime_ids:
#    users = get_usernames_from_comments(anime_id, token)
#    usernames_scraped += len(users)
#    print(usernames_scraped)
    # print(users)
