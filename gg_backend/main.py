from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import crud
import shutil
import os
#import bcrypt
from pydantic import BaseModel

# Konfiguration für JWT
SECRET_KEY = "Ihr_sehr_geheimer_Schlüssel"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Passwort-Kontext für Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer ist ein Abhängigkeits-Klasse, die die token URL erhält
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Dieses Modell definiert die Struktur der Token-Antwort
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    benutzername: str
    rolle: str
    



app = FastAPI()

origins = [
    "http://localhost:3000", #URL Frontend

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Die erlaubten HTTP-Methoden anpassen
    allow_headers=["*"],  # Hier können Sie die erlaubten Header anpassen
)


# Pfad zum Verzeichnis 'Fotosupload'
upload_folder = "Fotosupload"

# Erstellen Sie das Verzeichnis, wenn es nicht existiert
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# Mounten Sie nun das Verzeichnis
app.mount("/Fotosupload", StaticFiles(directory=upload_folder), name="Fotosupload")

# Hilfsfunktionen für Authentifizierung
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = crud.get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user["passwort"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Abhängigkeit, die den aktuellen Benutzer zurückgibt
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_data = crud.get_user_by_username(username)
    if user_data is None:
        raise credentials_exception

    # Erstellen Sie ein Benutzerobjekt aus den Datenbankdaten
    user = User(benutzername=user_data["benutzername"], rolle=user_data["rolle"]) 
    return user

# Endpunkt, um einen neuen Token zu bekommen
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["benutzername"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}



# Benutzer Endpunkte
@app.post("/benutzer/")
def create_benutzer(benutzername: str, email: str, passwort: str, current_user: User = Depends(get_current_user)):
    if current_user.rolle != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nicht autorisiert"
        )
    crud.create_benutzer(benutzername, email, passwort)
    return {"message": "Benutzer erstellt"}


@app.get("/benutzer/{benutzer_id}")
def read_benutzer(benutzer_id: int, current_user: User = Depends(get_current_user)):
    if current_user.rolle != 'admin':
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    benutzer = crud.get_benutzer(benutzer_id)
    if benutzer:
        return benutzer
    raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")

@app.put("/benutzer/{benutzer_id}")
def update_benutzer(benutzer_id: int, benutzername: str, email: str, passwort: str, current_user: User = Depends(get_current_user)):
    if current_user.rolle != 'admin':
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    crud.update_benutzer(benutzer_id, benutzername, email, passwort)
    return {"message": "Benutzer aktualisiert"}

@app.delete("/benutzer/{benutzer_id}")
def delete_benutzer(benutzer_id: int, current_user: User = Depends(get_current_user)):
    if current_user.rolle != 'admin':
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    crud.delete_benutzer(benutzer_id)
    return {"message": "Benutzer gelöscht"}


# Spielberichte Endpunkte
@app.post("/spielberichte/")
def create_spielbericht(titel: str, inhalt: str, spieldatum: str, erstelltvon: int, current_user: User = Depends(get_current_user)):
    if current_user.rolle not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    crud.create_spielbericht(titel, inhalt, spieldatum, erstelltvon)
    return {"message": "Spielbericht erstellt"}

@app.get("/spielberichte/{bericht_id}")
def read_spielbericht(bericht_id: int):
    bericht = crud.get_spielbericht(bericht_id)
    if bericht:
        return bericht
    raise HTTPException(status_code=404, detail="Spielbericht nicht gefunden")

@app.put("/spielberichte/{bericht_id}")
def update_spielbericht(bericht_id: int, titel: str, inhalt: str, spieldatum: str, current_user: User = Depends(get_current_user)):
    if current_user.rolle not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    crud.update_spielbericht(bericht_id, titel, inhalt, spieldatum)
    return {"message": "Spielbericht aktualisiert"}

@app.delete("/spielberichte/{bericht_id}")
def delete_spielbericht(bericht_id: int, current_user: User = Depends(get_current_user)):
    if current_user.rolle not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    crud.delete_spielbericht(bericht_id)
    return {"message": "Spielbericht gelöscht"}

# Fotos Endpunkte
@app.post("/fotos/")
def upload_foto(titel: str, beschreibung: str, hochgeladenvon: int, file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if current_user.rolle not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    # Ordner erstellen, wenn er nicht existiert
    folder = 'Fotosupload'
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    # Datei speichern
    file_location = f"{folder}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # URL generieren, über die das Bild erreichbar ist
    bildurl = f"http://localhost:8000/Fotosupload/{file.filename}"
    
    # Eintrag in der Datenbank erstellen
    crud.create_foto(titel, beschreibung, bildurl, hochgeladenvon)
    return {"message": "Foto erstellt", "bildurl": bildurl}

@app.get("/fotos/{foto_id}")
def read_foto(foto_id: int):
    foto = crud.get_foto(foto_id)
    if foto:
        return foto
    raise HTTPException(status_code=404, detail="Foto nicht gefunden")

@app.put("/fotos/{foto_id}")
def update_foto(foto_id: int, titel: str, beschreibung: str, bildurl: str, current_user: User = Depends(get_current_user)):
    if current_user.rolle not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    crud.update_foto(foto_id, titel, beschreibung, bildurl)
    return {"message": "Foto aktualisiert"}

@app.delete("/fotos/{foto_id}")
def delete_foto(foto_id: int, current_user: User = Depends(get_current_user)):
    if current_user.rolle not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    # Zuerst den Eintrag aus der Datenbank holen, um den Dateinamen zu erhalten
    foto = crud.get_foto(foto_id)
    if not foto:
        raise HTTPException(status_code=404, detail="Foto nicht gefunden")

    # Bild URL extrahieren und Dateinamen extrahieren
    bild_url = foto[3]  # Der Index für 'bildurl' ist 3, basierend auf Ihrer Tabelle
    filename = bild_url.split("/")[-1]  # Der Dateiname ist der letzte Teil der URL
    file_path = f"Fotosupload/{filename}"

    # Versuchen, die Datei zu löschen
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Löschen der Bilddatei: {e}")

    # Datenbankeintrag löschen
    crud.delete_foto(foto_id)

    return {"message": "Foto gelöscht"}



# Spiele Endpunkte
@app.post("/spiele/")
def create_spiel(gegner: str, spieldatum: str, ort: str, ergebnis: str, current_user: User = Depends(get_current_user)):
    if current_user.rolle not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    crud.create_spiel(gegner, spieldatum, ort, ergebnis)
    return {"message": "Spiel erstellt"}

@app.get("/spiele/{spiel_id}")
def read_spiel(spiel_id: int):
    spiel = crud.get_spiel(spiel_id)
    if spiel:
        return spiel
    raise HTTPException(status_code=404, detail="Spiel nicht gefunden")

@app.put("/spiele/{spiel_id}")
def update_spiel(spiel_id: int, gegner: str, spieldatum: str, ort: str, ergebnis: str, current_user: User = Depends(get_current_user)):
    if current_user.rolle not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    crud.update_spiel(spiel_id, gegner, spieldatum, ort, ergebnis)
    return {"message": "Spiel aktualisiert"}

@app.delete("/spiele/{spiel_id}")
def delete_spiel(spiel_id: int, current_user: User = Depends(get_current_user)):
    if current_user.rolle not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Nicht autorisiert")
    crud.delete_spiel(spiel_id)
    return {"message": "Spiel gelöscht"}


