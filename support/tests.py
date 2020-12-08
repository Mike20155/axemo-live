
import hashlib
import random
# Create your models here



id =  random.randint(1, 100000000000000)
crypt = hashlib.sha256(str(id).encode()).hexdigest()[:10]
print(crypt)