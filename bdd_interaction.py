import mysql.connector

def connect_to_bdd():
    connect = mysql.connector.connect(
        host="nakamadb.c1ikgo6w654z.eu-north-1.rds.amazonaws.com",
        user="admin",
        password="Dul70623",
        database="nakamaBDD"
    )

    return connect



def add_user_to_BDD(username_to_add):
    sql_connector=connect_to_bdd()
    cursor = sql_connector.cursor()

    insert_query = "INSERT INTO Extracted_usernames (username) VALUES (%s)"
    data = (username_to_add,)

    try:
        cursor.execute(insert_query, data)
        sql_connector.commit()
        print(f"Utilisateur {username_to_add} ajouté.")
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

       # for username in usernames:
       #     print(username[0])

    except mysql.connector.Error as err:
        print(f"Erreur : {err}")

    cursor.close()
    sql_connector.close()

    return usernames

