import requests

def req_breach(pseudo, output_file):
    key = ""
    url = f"https://BreachDirectory.com/api_usage?method=username&key={key}&query={pseudo}"
    response = requests.get(url)

    if response.ok:
        data = response.json()

        with open(output_file, "a") as file:
            for entry in data:
                # Vérifier la présence des champs nécessaires
                if 'domain' in entry and entry['domain'] and 'email' in entry and entry['email'] and 'username' in entry and entry['username']:
                    title = entry.get('title', 'N/A')
                    domain = entry['domain']
                    email = entry['email']
                    username = entry['username']
                    ip = entry.get('ip', 'N/A')

                    # Écrire dans le fichier uniquement si tous les champs sont présents
                    print(f"Title: {title}, Domain: {domain}, Email: {email}, Username: {username}, IP: {ip}", file=file)
    else:
        print(f"Erreur de requête : {response.status_code}")
        print(f"Message d'erreur : {response.text}")