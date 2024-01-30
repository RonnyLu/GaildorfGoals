import psycopg2
from .database import get_database_connection
from passlib.context import CryptContext
#Test

# Erstellen Sie eine Instanz von CryptContext für die Passwort-Hash-Funktionen
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(username):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM benutzer WHERE benutzername = %s", (username,))
        user = cursor.fetchone()
        return user
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Create
# Verwenden Sie pwd_context.hash, um das Passwort zu hashen
def create_benutzer(benutzername, email, passwort, rolle='user'):
    hashed_password = pwd_context.hash(passwort)
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO benutzer (benutzername, email, passwort, rolle) VALUES (%s, %s, %s, %s)", (benutzername, email, hashed_password, rolle))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Read
def get_benutzer(benutzer_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM benutzer WHERE benutzerid = %s", (benutzer_id,))
        benutzer = cursor.fetchone()
        return benutzer
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Update
# Verwenden Sie pwd_context.hash beim Aktualisieren des Passworts
def update_benutzer(benutzer_id, benutzername, email, passwort):
    hashed_password = pwd_context.hash(passwort)
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE benutzer SET benutzername = %s, email = %s, passwort = %s WHERE benutzerid = %s", (benutzername, email, hashed_password, benutzer_id))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Delete
def delete_benutzer(benutzer_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM benutzer WHERE benutzerid = %s", (benutzer_id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

#Passwort hashen
# Verwenden Sie pwd_context.verify, um das Passwort zu überprüfen
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# CRUD für Spielberichte

def create_spielbericht(titel, inhalt, spieldatum, erstelltvon):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO spielberichte (titel, inhalt, spieldatum, erstelltvon) VALUES (%s, %s, %s, %s)", (titel, inhalt, spieldatum, erstelltvon))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_spielbericht(bericht_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM spielberichte WHERE berichtid = %s", (bericht_id,))
        bericht = cursor.fetchone()
        return bericht
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_spielbericht(bericht_id, titel, inhalt, spieldatum):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE spielberichte SET titel = %s, inhalt = %s, spieldatum = %s WHERE berichtid = %s", (titel, inhalt, spieldatum, bericht_id))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def delete_spielbericht(bericht_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM spielberichte WHERE berichtid = %s", (bericht_id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# CRUD für Fotos

def create_foto(titel, beschreibung, bildurl, hochgeladenvon):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO fotos (titel, beschreibung, bildurl, hochgeladenvon) VALUES (%s, %s, %s, %s)", (titel, beschreibung, bildurl, hochgeladenvon))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_foto(foto_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM fotos WHERE fotoid = %s", (foto_id,))
        foto = cursor.fetchone()
        return foto
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_foto(foto_id, titel, beschreibung, bildurl):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE fotos SET titel = %s, beschreibung = %s, bildurl = %s WHERE fotoid = %s", (titel, beschreibung, bildurl, foto_id))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def delete_foto(foto_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM fotos WHERE fotoid = %s", (foto_id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()



# CRUD für Spiele

def create_spiel(gegner, spieldatum, ort, ergebnis):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO spiele (gegner, spieldatum, ort, ergebnis) VALUES (%s, %s, %s, %s)", (gegner, spieldatum, ort, ergebnis))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_spiel(spiel_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM spiele WHERE spielid = %s", (spiel_id,))
        spiel = cursor.fetchone()
        return spiel
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_spiel(spiel_id, gegner, spieldatum, ort, ergebnis):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE spiele SET gegner = %s, spieldatum = %s, ort = %s, ergebnis = %s WHERE spielid = %s", (gegner, spieldatum, ort, ergebnis, spiel_id))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def delete_spiel(spiel_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM spiele WHERE spielid = %s", (spiel_id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

