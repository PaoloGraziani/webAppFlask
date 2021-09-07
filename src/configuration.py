import hashlib
import random
import time
def SECRET():
    date = time.strftime("%d/%m/%Y %H:%M:%S")
    cip = random.randint(1000,9999)
    secret_key = str(date) +' '+ str(cip)
    h = hashlib.md5(secret_key.encode())
    secret_key = h.hexdigest()
    return secret_key
SESSION_TYPE = 'filesystem'