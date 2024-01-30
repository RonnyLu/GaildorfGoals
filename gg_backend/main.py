from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Optional
from . import crud
import shutil
import os

app = FastAPI()

# Angenommen, Ihre Fotos werden im Verzeichnis 'uploads' im Wurzelverzeichnis des Projekts gespeichert
app.mount("/Fotosupload", StaticFiles(directory="Fotosupload"), name="Fotosupload")

# Benutzer Endpunkte
@app.post("/benutzer/")
def create_benutzer(benutzername: str, email: str, passwort: str):
    crud.create_benutzer(benutzername, email, passwort)
    return {"message": "Benutzer erstellt"}

@app.get("/benutzer/{benutzer_id}")
def read_benutzer(benutzer_id: int):
    benutzer = crud.get_benutzer(benutzer_id)
    if benutzer:
        return benutzer
    raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")

@app.put("/benutzer/{benutzer_id}")
def update_benutzer(benutzer_id: int, benutzername: str, email: str, passwort: str):
    crud.update_benutzer(benutzer_id, benutzername, email, passwort)
    return {"message": "Benutzer aktualisiert"}

@app.delete("/benutzer/{benutzer_id}")
def delete_benutzer(benutzer_id: int):
    crud.delete_benutzer(benutzer_id)
    return {"message": "Benutzer gelöscht"}


# Spielberichte Endpunkte
@app.post("/spielberichte/")
def create_spielbericht(titel: str, inhalt: str, spieldatum: str, erstelltvon: int):
    crud.create_spielbericht(titel, inhalt, spieldatum, erstelltvon)
    return {"message": "Spielbericht erstellt"}

@app.get("/spielberichte/{bericht_id}")
def read_spielbericht(bericht_id: int):
    bericht = crud.get_spielbericht(bericht_id)
    if bericht:
        return bericht
    raise HTTPException(status_code=404, detail="Spielbericht nicht gefunden")

@app.put("/spielberichte/{bericht_id}")
def update_spielbericht(bericht_id: int, titel: str, inhalt: str, spieldatum: str):
    crud.update_spielbericht(bericht_id, titel, inhalt, spieldatum)
    return {"message": "Spielbericht aktualisiert"}

@app.delete("/spielberichte/{bericht_id}")
def delete_spielbericht(bericht_id: int):
    crud.delete_spielbericht(bericht_id)
    return {"message": "Spielbericht gelöscht"}

# Fotos Endpunkte
@app.post("/fotos/")
async def upload_foto(titel: str, beschreibung: str, hochgeladenvon: int, file: UploadFile = File(...)):
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
def update_foto(foto_id: int, titel: str, beschreibung: str, bildurl: str):
    crud.update_foto(foto_id, titel, beschreibung, bildurl)
    return {"message": "Foto aktualisiert"}

@app.delete("/fotos/{foto_id}")
def delete_foto(foto_id: int):
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
def create_spiel(gegner: str, spieldatum: str, ort: str, ergebnis: str):
    crud.create_spiel(gegner, spieldatum, ort, ergebnis)
    return {"message": "Spiel erstellt"}

@app.get("/spiele/{spiel_id}")
def read_spiel(spiel_id: int):
    spiel = crud.get_spiel(spiel_id)
    if spiel:
        return spiel
    raise HTTPException(status_code=404, detail="Spiel nicht gefunden")

@app.put("/spiele/{spiel_id}")
def update_spiel(spiel_id: int, gegner: str, spieldatum: str, ort: str, ergebnis: str):
    crud.update_spiel(spiel_id, gegner, spieldatum, ort, ergebnis)
    return {"message": "Spiel aktualisiert"}

@app.delete("/spiele/{spiel_id}")
def delete_spiel(spiel_id: int):
    crud.delete_spiel(spiel_id)
    return {"message": "Spiel gelöscht"}

# Weitere Endpunkte und Funktionalitäten können hier hinzugefügt werden
