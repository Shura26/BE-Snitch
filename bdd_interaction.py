import mysql.connector
import os
def connect_to_bdd():
    connect = mysql.connector.connect(
        host="be-snitch-database.cj0k0segk76y.eu-west-3.rds.amazonaws.com",
        user="admin",
        password=os.environ.get('PASSWORD_BDD'),
        database="besnitch"
    )

    return connect


def add_to_BDD(value_to_add, table, column):

    #Si  existe pas, ajoute a la BDD
    if check_exists(value_to_add,table, column) == False:
        sql_connector = connect_to_bdd()
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




def get_user_in_BDD():
    sql_connector = connect_to_bdd()
    cursor = sql_connector.cursor()

    select_query = "SELECT username FROM Extracted_usernames"

    try:
        cursor.execute(select_query)
        usernames = cursor.fetchall()

        # debug affih usernames in BDD
        #for username in usernames:
            #print(username[0])

    except mysql.connector.Error as err:
        print(f"Erreur : {err}")

    cursor.close()
    sql_connector.close()

    return usernames



def clear_all_users():
    sql_connector = connect_to_bdd()
    cursor = sql_connector.cursor()

    delete_query = "DELETE FROM id_checked"

    try:
        cursor.execute(delete_query)
        sql_connector.commit()
        print("Tous les utilisateurs ont été supprimés avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")
        sql_connector.rollback()

    cursor.close()
    sql_connector.close()


def check_exists(value_to_check, table, column):
    sql_connector = connect_to_bdd()
    cursor = sql_connector.cursor()

    select_query = f"SELECT {column} FROM {table} WHERE {column} = %s"
    data = (value_to_check,)

    try:
        cursor.execute(select_query, data)
        existing_value = cursor.fetchone()

        if existing_value:
            print(f"{value_to_check} existe dans la BDD.")
            return True
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Erreur : {err}")

    cursor.close()
    sql_connector.close()

