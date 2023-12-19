import requests

def req_breach(pseudo, output_file):
    #API KEY
    key = ""
    url = "https://BreachDirectory.com/api_usage?method=username&key=" + key + "&query=" + pseudo
    response = requests.get(url)

    if response.ok:
        data = response.json()

        with open(output_file, "a") as file:

            for entry in data:
                title = entry['title']
                domain = entry['domain']
                email = entry['email']
                username = entry['username']
                ip = entry['ip']


                print(f"Title: {title}, Domain: {domain}, Email: {email}, Username: {username}, IP: {ip}", file=file)

    else:
        print(f"Erreur de requête : {response.status_code}")
        print(f"Message d'erreur : {response.text}")

