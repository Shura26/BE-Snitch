import mysql.connector, os
from mail import *


def connect_to_bdd():
    connect = mysql.connector.connect(
        host="be-snitch-database.cj0k0segk76y.eu-west-3.rds.amazonaws.com",
        user="admin",
        password=os.environ.get('PASSWORD_BDD'),
        database="besnitch"
    )

    return connect

#Fonctions pour ajouter des éléments a la base de données
def add_to_BDD(value_to_add, table, column):
    sql_connector = connect_to_bdd()

    # Si  existe pas, ajoute a la BDD
    if check_exists(sql_connector, value_to_add, table, column) == False:
        cursor = sql_connector.cursor()

        insert_query = f"INSERT INTO {table} ({column}) VALUES (%s)"
        data = (value_to_add,)

        try:
            cursor.execute(insert_query, data)
            sql_connector.commit()
            print(f"{value_to_add} ajouté dans la BDD.")
        except mysql.connector.Error as err:
            print(f"Erreur : {err}")
            sql_connector.rollback()

        cursor.close()
        sql_connector.close()
    else:
        print("User already exist")


#Ajouter les username, email et domaine retourner par breachdirectory a la BDD
def add_compromised_user(username, email, domain):
    sql_connector = connect_to_bdd()
    cursor = sql_connector.cursor()
    # si pas de doublon
    if check_exists(sql_connector, email, "compromised_user", "mail_user_compromised") == False:
        if check_exists(sql_connector, email, "email_already_send", "mail") == False:

            insert_query = "INSERT INTO compromised_user (compromised_username, mail_user_compromised, domain_from) VALUES (%s, %s, %s)"
            data = (username, email, domain)

            try:
                cursor.execute(insert_query, data)
                sql_connector.commit()

            except mysql.connector.Error as err:
                print(f"Erreur : {err}")
                sql_connector.rollback()

    cursor.close()
    sql_connector.close()



#Extraire les users compromis de la BDD
def get_compromised_user_info():
    sql_connector = connect_to_bdd()
    cursor = sql_connector.cursor()

    select_query = "SELECT * FROM compromised_user"

    try:
        cursor.execute(select_query)
        compromised_users = cursor.fetchall()

        # Récupère les infos sur l'utilisateur
        for user in compromised_users:
            id_user_compromised = user[0]
            compromised_username = user[1]
            mail_user_compromised = user[2]
            domain_from = user[3]
            # si email pas dans mail_already_send
            if check_exists(sql_connector, mail_user_compromised, "email_already_send", "mail") == False:
                mail_sender(compromised_username, mail_user_compromised, domain_from)

                # Met le mail dans la table mail_already_send
                insert_query = "INSERT INTO email_already_send (mail) VALUES (%s)"
                cursor.execute(insert_query, (mail_user_compromised,))

        # Valide les modif
        sql_connector.commit()

    except mysql.connector.Error as err:
        print(f"Erreur : {err}")
        # si erreur annule le commit
        sql_connector.rollback()

    cursor.close()
    sql_connector.close()



#Vérifier si un élément existe dans la BDD
def check_exists(sql_connector, value_to_check, table, column):
    cursor = sql_connector.cursor()

    select_query = f"SELECT {column} FROM {table} WHERE {column} = %s"
    data = (value_to_check,)

    try:
        cursor.execute(select_query, data)
        existing_value = cursor.fetchone()

        if existing_value:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Erreur : {err}")

    cursor.close()
    sql_connector.close()


def check_user_exists(sql_connector, table, login, password, value_to_check=None):
    cursor = sql_connector.cursor()

    select_query = f"SELECT account_id, prenom FROM {table} WHERE prenom = '{login}' AND password = '{password}'"

    try:
        cursor.execute(select_query)
        existing_user = cursor.fetchone()
        print(existing_user)
        if existing_user:
            user_id, login = existing_user
            print(f"{value_to_check} existe dans la BDD. ID: {user_id}, Prénom: {login}")
            return {"account_id": user_id, "prenom": login}
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Erreur : {err}")

    finally:
        cursor.close()


def get_ids_already_checked(sql_connector):
    cursor = sql_connector.cursor()
    query = "SELECT anime_id FROM crunchyroll_ids_checked;"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        sql_connector.commit()
        return result
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")
        sql_connector.rollback()
    finally:
        cursor.close()
        sql_connector.close()


# récupère le starting_id nécessaire a la récupération des pseudos d'adn
def get_starting_id():
    sql_connector = connect_to_bdd()
    cursor = sql_connector.cursor()
    query = "SELECT id FROM adn_starting_id;"

    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")
        sql_connector.rollback()
    finally:
        cursor.close()
        sql_connector.close()


# mets à jour le starting_id nécessaire a la récupération des pseudos d'adn
def update_adn_starting_id(starting_id):
    sql_connector = connect_to_bdd()
    cursor = sql_connector.cursor()
    query = "UPDATE adn_starting_id SET id = %s;"

    try:
        cursor.execute(query, (starting_id,))
        sql_connector.commit()
        print("Starting ID updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sql_connector.rollback()
    finally:
        cursor.close()


# return les pseudos
def get_user_in_BDD(bdd):
    sql_connector = connect_to_bdd()
    cursor = sql_connector.cursor()

    select_query = f"SELECT pseudo FROM {bdd};"

    try:
        cursor.execute(select_query)
        usernames = cursor.fetchall()

        # debug affih usernames in BDD
        # for username in usernames:
        # print(username[0])

    except mysql.connector.Error as err:
        print(f"Erreur : {err}")

    cursor.close()
    sql_connector.close()

    return usernames


def reinitialise_table(table):
    sql_connector = connect_to_bdd()
    cursor = sql_connector.cursor()

    delete_query = f"DELETE FROM {table};"

    try:
        cursor.execute(delete_query)
        sql_connector.commit()
        print(f"Toutes les données de la table {table} ont été supprimées.")
    except mysql.connector.Error as err:
        sql_connector.rollback()
        print(f"Erreur lors de la suppression des données : {err}")
    finally:
        cursor.close()
        sql_connector.close()
