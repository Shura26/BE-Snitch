from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, current_user, login_user, logout_user
from scope.adn.get_usernames import *
from scope.crunchyroll.get_usernames import *
from breachdirectory import *
from BDD.scripts.adn import *
from BDD.scripts.crunchyroll import *
from mail import *
from User import User
import uuid

################################################################  CONFIG FLASK ############################################################


app = Flask(__name__)

# Configuration pour la gestion des sessions (à remplacer par une méthode plus sécurisée en production)
app.secret_key = 'abe4cd4b3e2384ea93cf8966097e1cD3cdc9032f69c2829a'
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(prenom):
    '''
    user_data = requete dans la bdd pour trouver le prenom=prenom
    if user_data:
        return User(
            prenom=user_data['prenom']
        )
    return None
   '''
    uuid_value = uuid.uuid4() 
    return User(user_id=uuid_value, prenom=prenom)


################################################################  ROUTES AUTHENTIFICATION ############################################################

# Page d'accueil avec les boutons pour lancer les scripts
@app.route('/')
def index():
    if current_user.is_authenticated:
        print("dd")
        return render_template('index.html')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Vérification des informations de connexion
        prenom = request.form['prenom']
        password = request.form['password']

        # vérification simple (à remplacer par notre vérification sécurisée)
        if prenom == 'utilisateur' and password == 'passe':
            user = load_user(prenom)
            login_user(user)
            session['logged_in'] = True
            return redirect(url_for('index'))

    return render_template('login.html')


# Déconnexion
@app.route('/logout')
def logout():
    logout_user()
    session.pop('logged_in', None)
    return redirect(url_for('index'))

################################################################  FONCTIONNALITES ############################################################

@app.route('/recuperer_pseudos_crunchyroll', methods=['POST'])
def recuperer_pseudos_crunchyroll():
    limit_ids = request.form['limit_ids']
    token = get_access_token()
    anime_ids = get_lastest_anime_ids(token, int(limit_ids))
    get_pseudos_from_crunchyroll(anime_ids, token)
    #implémenter la suite de la logique avec breachdirectory

@app.route('/recuperer_pseudos_adn', methods=['POST'])
def recuperer_pseudos_adn():
    limit_call = request.form['limit_call']
    starting_id = get_starting_id()
    get_username_from_adn(starting_id, int(limit_call))
    #implémenter la suite de la logique avec breachdirectory

@app.route('/envoyer_mail', methods=['POST'])
def envoyer_mail():
    mail_sender()


################################################################  MAIN ############################################################

if __name__ == '__main__':
    app.run(debug=True)
