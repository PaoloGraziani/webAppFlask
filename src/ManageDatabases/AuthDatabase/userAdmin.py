import psycopg2
import hashlib
from src.ManageDatabases.settingDatabase import Authentication_HOST, Authentication_DATABASE, Authentication_USERNAME, \
    Authentication_PASSWORD, closeCursor, connectDatabase, closeConnection


def username_password_confirm(username, password):
    h = hashlib.md5(password.encode())
    password = h.hexdigest()
    #print(password)
    connessione = connectDatabase(Authentication_HOST, Authentication_DATABASE, Authentication_USERNAME,
                                  Authentication_PASSWORD)
    valid = 0
    with connessione.cursor() as cursore:
        #print(str(password))
        cursore.execute("SELECT * FROM USERS WHERE id_user=%s AND pass=%s", (username, str(password)))
        if cursore.fetchone() == None:
            valid = False
        else:
            valid = True
        closeCursor(cursore)
    closeConnection(connessione)
    return valid

def role_user(username, password):
    h = hashlib.md5(password.encode())
    password = h.hexdigest()
    print(password)
    connessione = connectDatabase(Authentication_HOST, Authentication_DATABASE, Authentication_USERNAME,
                                  Authentication_PASSWORD)
    with connessione.cursor() as ruolo:
        ruolo.execute("SELECT ruolo FROM USERS WHERE id_user=%s AND pass=%s", (username, str(password)))
        sel_role = ruolo.fetchone()[0]

        closeCursor(ruolo)
    closeConnection(connessione)
    return sel_role


