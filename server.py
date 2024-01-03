from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, current_user, login_user, logout_user
from scope.adn.get_usernames import *
from scope.crunchyroll.get_usernames import *
from breachdirectory import *
from mail import *
from User import User
import uuid, os

################################################################  CONFIG FLASK ############################################################


app = Flask(__name__)

# Configuration pour la gestion des sessions
app.secret_key = os.environ.get('SESSION_SECRET_FLASK')
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id_account):

    return User(
        user_id=id_account
    )


################################################################  ROUTES AUTHENTIFICATION ############################################################

# Page d'accueil avec les boutons pour lancer les scripts
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Vérification des informations de connexion
        login_name = request.form['login']
        password = request.form['password']

        user_exist = check_user_exists(bdd_connection, 'accounts', login_name, password)
        print("dfsdfdsf")
        if user_exist:
            user = load_user(user_exist["account_id"])
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
    users = get_pseudos_from_crunchyroll(anime_ids, token)
    if users:
        for user in users:
            req_breach(user)
            print(f"Breach req for: {user}")

    return render_template('index.html', derniers_ajouts=users)


@app.route('/recuperer_pseudos_adn', methods=['POST'])
def recuperer_pseudos_adn():
    limit_call = request.form['limit_call']
    starting_id = get_starting_id()
    users = get_username_from_adn(starting_id, int(limit_call))
    if users:
        for user in users:
            add_to_BDD(user,"adn_pseudos","pseudo")
            req_breach(user)
            print(f"Breach req for: {user}")

    return render_template('index.html', derniers_ajouts=users)


@app.route('/delete_adn', methods=['POST'])
def delete_adn():
    reinitialise_table("adn_pseudos")
    update_adn_starting_id(699)

    return render_template('index.html')


@app.route('/delete_crunchyroll', methods=['POST'])
def delete_crunchyroll():
    reinitialise_table("crunchyroll_pseudos")
    reinitialise_table("crunchyroll_ids_checked")

    return render_template('index.html')

@app.route('/envoyer_mail', methods=['POST'])
def envoyer_mail():
    get_compromised_user_info()
    return render_template('index.html')


################################################################  MAIN ############################################################

if __name__ == '__main__':
    bdd_connection = connect_to_bdd()
    app.run(debug=True)
