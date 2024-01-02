import os
import smtplib, ssl
from email.message import EmailMessage


#ouvre un fichier contenant les info des user sous forme : "Title: Nom_Site, Domain: Nom_site, Email: email_user, Username: username"
#et envoie un mail pour chaque user présent dans le fichier
#a addapter plus tard quand il y aura la BBD

def mail_sender() :
    mail = "nakamaprotect@outlook.fr"
    password = os.environ.get('PASSWORD_MAIL')

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