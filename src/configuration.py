import hashlib
import random
import time
date = time.strftime("%d/%m/%Y")
cip = random.randint(1000,9999)
secret_key = str(date) + str(cip)
h = hashlib.md5(secret_key.encode())
secret_key = h.hexdigest()
SECRET = secret_key  # metti su un file di configurazione
SECRET_TYPE='filesystem'