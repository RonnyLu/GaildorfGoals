from passlib.context import CryptContext
from main import get_password_hash, verify_password


# Passwort-Kontext erstellen
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Passwort, das gehasht werden soll
#raw_password = "Timo"

# Passwort hashen
##hashed_password = pwd_context.hash(raw_password)

#print("Gehashtes Passwort:", hashed_password)


#test_password = "Timo"
#hashed_password = get_password_hash(test_password)
#print(hashed_password)

#test_password = "Ronny"
#hashed_password = get_password_hash(test_password)
#is_valid = verify_password(test_password, hashed_password)
#print(is_valid)  # Sollte True ausgeben

test_password = "Neu"
hashed_password = get_password_hash(test_password)
print("Gehashtes Passwort:", hashed_password)

is_valid = verify_password(test_password, hashed_password)
print("Ist das Passwort gültig:", is_valid)  # Erwartetes Ergebnis: True

