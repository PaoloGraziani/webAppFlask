import psycopg2

'''
Inizializzazione DATABASE di Autenticazione
'''
Authentication_HOST = "localhost"
Authentication_DATABASE = "AuthDATA"
Authentication_USERNAME = "postgres"
Authentication_PASSWORD = "postgres"

'''
Inizializzazione DATABASE di Applicazione
'''
Application_HOST = "localhost"
Application_DATABASE = "DbWebApp"
Application_USERNAME = "postgres"
Application_PASSWORD = "postgres"


def closeCursor(cur):
    cur.close()


def connectDatabase(host, database, username, password):
    newConnection = psycopg2.connect(host=host, database=database, user=username, password=password)
    return newConnection


def closeConnection(conn):
    conn.close()
