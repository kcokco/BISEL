import sys
import os
import random

# Hozzáadjuk a projekt főkönyvtárát a rendszer útvonalához (sys.path),
# így a pytest futtatásakor megtalálja a szülő mappában lévő main.py-t.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

# Létrehozunk egy teszt kliens példányt a FastAPI alkalmazásunk alapján.
# Ez szimulálja a HTTP kéréseket (GET, POST stb.) anélkül, hogy ténylegesen
# el kellene indítanunk a szervert (uvicorn).
client = TestClient(app)

# A pytest minden olyan függvényt automatikusan futtat, aminek a neve 'test_'-tel kezdődik.
def test_read_root():
    # Küldünk egy szimulált GET kérést a főoldalra ("/")
    response = client.get("/")
    
    # Ellenőrizzük, hogy a válaszkód 200 (Sikeres)
    assert response.status_code == 200
    
    # Ellenőrizzük, hogy a kapott JSON válasz pontosan megegyezik-e az elvárttal
    assert response.json() == {"message": "Üdvözöl a BISEL projekt webes API-ja! Minden sikeresen elindult!"}

def test_create_and_read_user():
    # 1. LÉPÉS: Új felhasználó létrehozása (POST kérés)
    # Generálunk egy egyedi email címet, hogy ne legyen ütközés az adatbázisban a többszöri tesztelésnél.
    test_email = f"teszt.elek_{random.randint(10000, 99999)}@pelda.hu"
    
    # A regisztrációs űrlaphoz (UserCreate schema) szükséges adatok
    user_data = {
        "email": test_email,
        "password": "titkosjelszo123",
        "name": "Teszt Elek"
    }
    
    # Elküldjük a POST kérést a /users/ végpontra a fenti adatokkal (JSON formátumban)
    response_create = client.post("/users/", json=user_data)
    
    # Ellenőrizzük, hogy sikeresen létrejött-e
    assert response_create.status_code == 200, f"Hiba a létrehozásnál: {response_create.text}"
    
    # Kinyerjük a választ JSON-ként (ez már egy User schema formátum kell legyen)
    created_user = response_create.json()
    
    # Ellenőrizzük az elvárt mezőket
    assert created_user["email"] == test_email
    assert "id" in created_user
    
    # Eltároljuk az azonosítót a 2. lépéshez
    new_user_id = created_user["id"]

    # 2. LÉPÉS: Az újonnan létrehozott felhasználó lekérdezése (GET kérés)
    response_read = client.get(f"/users/{new_user_id}")
    
    # Ellenőrizzük a státuszkódot
    assert response_read.status_code == 200
    
    # Ellenőrizzük, hogy ugyanazt a felhasználót kaptuk-e vissza
    fetched_user = response_read.json()
    assert fetched_user["id"] == new_user_id
    assert fetched_user["email"] == test_email

