import os
import smtplib, ssl
from email.message import EmailMessage
from bdd_interaction import *


#Utilisation d'un relais outlook pour envoyer les mails
#pour pas que le mail fini dans les spam
def mail_sender(username, email, domain) :
    mail = "nakamaprotect@outlook.fr"
    password = os.environ.get('PASSWORD_MAIL')
    print(f"email envoyer a : {email}")

    msg = EmailMessage()
    msg.set_content(
        "Cher(e) utilisateur(trice), \n\n\n"
        "Nous sommes NakamaProtect, une organisation à but non lucratif dédiée à la préservation de la confidentialité des comptes utilisateurs en ligne."
        "\n\nNous souhaitons vous informer que nous avons récemment identifié une possible compromission d'identifiants associés à votre compte sous l'identifiant " + username + ". "
        "\n\nLa fuite de vos données provient des sources suivantes : " + domain + "."
        "\n\nNous vous conseillons de ne plus utiliser ce mot de passe et changer tous vos accès l'utilisant."
        "\n\nSi vous n'êtes pas concerné par ce mail, nous nous excusons de la gêne occasionnée."
        "\n\n\nCordialement,\nL'équipe Nakamaprotect")

    msg["Subject"] = "Nakamaprotect"
    msg["From"] = "nakamaprotect@outlook.fr"
    msg["To"] = email

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.office365.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(msg["From"], password)
        smtp.send_message(msg)




