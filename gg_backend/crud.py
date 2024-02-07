import psycopg2
from database import get_database_connection
from passlib.context import CryptContext


# Erstellen Sie eine Instanz von CryptContext für die Passwort-Hash-Funktionen
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(username):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM benutzer WHERE benutzername = %s", (username,))
        user_row = cursor.fetchone()
        if user_row:
            user = {
                "benutzerid": user_row[0],
                "benutzername": user_row[1],
                "passwort": user_row[2],
                "email": user_row[3],
                "rolle": user_row[4]
            }
            return user
        return None
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


# Erstellen Sie eine Instanz von CryptContext für die Passwort-Hash-Funktionen
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(username):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM benutzer WHERE benutzername = %s", (username,))
        user_row = cursor.fetchone()
        if user_row:
            user = {
                "benutzerid": user_row[0],
                "benutzername": user_row[1],
                "passwort": user_row[2],
                "email": user_row[3],
                "rolle": user_row[4]
            }
            return user
        return None
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


# CRUD für Berichte


def get_all_berichte():
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT berichtid, titel, gegner, ergebnis, ort, spieldatum FROM berichte")
        berichte = cursor.fetchall()
        
        # Formatieren Sie die Ergebnisse in ein benutzerdefiniertes Datenformat
        berichte_list = []
        for bericht in berichte:
            berichte_list.append({
                "berichtid": bericht[0],  # Fügen Sie berichtid hier hinzu
                "titel": bericht[1],
                "gegner": bericht[2],
                "ergebnis": bericht[3],
                "ort": bericht[4],
                "spieldatum": bericht[5]
            })
        
        return berichte_list
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def create_bericht(titel, gegner, ergebnis, ort, inhalt, spieldatum, erstelltvon):
    # Überprüfen, ob alle erforderlichen Felder ausgefüllt sind
    if not titel or not gegner or not ergebnis or not ort or not inhalt or not spieldatum or not erstelltvon:
        return False

    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO berichte (titel, gegner, ergebnis, ort, inhalt, spieldatum, erstelltvon) VALUES (%s, %s, %s, %s, %s, %s, %s)", (titel, gegner, ergebnis, ort, inhalt, spieldatum, erstelltvon))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_bericht(bericht_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM berichte WHERE berichtid = %s", (bericht_id,))
        bericht = cursor.fetchone()
        return bericht
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


# Update
def update_bericht(bericht_id, titel, gegner, ergebnis, ort, inhalt, spieldatum):
    # Überprüfen, ob alle erforderlichen Felder ausgefüllt sind
    if not titel or not gegner or not ergebnis or not ort or not inhalt or not spieldatum:
        return False

    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE berichte SET titel = %s, gegner = %s, ergebnis = %s, ort = %s, inhalt = %s, spieldatum = %s WHERE berichtid = %s", (titel, gegner, ergebnis, ort, inhalt, spieldatum, bericht_id))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def delete_bericht(bericht_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM berichte WHERE berichtid = %s", (bericht_id,))
        conn.commit()
        return True  # Erfolgreich gelöscht
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        conn.rollback()
        return False  # Nicht gefunden oder Fehler beim Löschen
    finally:
        cursor.close()
        conn.close()








# CRUD für Fotos

def get_all_fotos():
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT fotoid, titel, bildurl FROM fotos")
        fotos = cursor.fetchall()
        
        # Formatieren Sie die Ergebnisse in ein benutzerdefiniertes Datenformat
        fotos_list = []
        for foto in fotos:
            fotos_list.append({
                "fotoid": foto[0],  
                "titel": foto[1],
                "bildurl": foto[2],
            })
        
        return fotos_list
    except psycopg2.Error as e:
        print(f"Fehler: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

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