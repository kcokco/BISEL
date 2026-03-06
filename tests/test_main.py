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
    data = response_create.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    # Jelszót soha nem adunk vissza, így az nem lehet benne a válaszban
    assert "password" not in data
    assert "hashed_password" not in data
    
    # Eltároljuk az azonosítót a 2. lépéshez
    new_user_id = data["id"]

    # 2. LÉPÉS: Az újonnan létrehozott felhasználó lekérdezése (GET kérés)
    response_read = client.get(f"/users/{new_user_id}")
    
    # Ellenőrizzük a státuszkódot
    assert response_read.status_code == 200
    
    # Ellenőrizzük, hogy ugyanazt a felhasználót kaptuk-e vissza
    fetched_user = response_read.json()
    assert fetched_user["id"] == new_user_id
    assert fetched_user["email"] == test_email

def test_login_and_get_reports():
    """
    1. Létrehoz egy új felhasználót (vagy használ egy létezőt)
    2. Bejelentkezik a /users/login végponton, és kap egy JWT tokent
    3. Lekérdezi a védett /reports/me végpontot a tokennel
    """
    import uuid
    email = f"auth_test_{uuid.uuid4().hex[:8]}@example.com"
    password = "SuperSecretPassword123!"

    # 1. Regisztráció
    client.post("/users/", json={
        "name": "Auth Tester",
        "email": email,
        "password": password
    })

    # 2. Bejelentkezés (x-www-form-urlencoded formátum!)
    login_response = client.post(
        "/users/login",
        data={"username": email, "password": password}
    )
    assert login_response.status_code == 200, login_response.text
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    token = token_data["access_token"]

    # 3. Védett végpont hívása (Authorization: Bearer <token>)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Új jelentés létrehozása
    report_response = client.post(
        "/reports/",
        json={
            "watercourse_id": "Test River",
            "sampling_site_id": "Bridge 1",
            "date": "2024-06-01",
            "bisel_index": 7
        },
        headers=headers
    )
    assert report_response.status_code == 200, report_response.text

    # Lekérdezés a /me végpontról
    me_response = client.get("/reports/me", headers=headers)
    assert me_response.status_code == 200, me_response.text
    my_reports = me_response.json()
    
    # Bizonyítjuk, hogy legalább 1 mérése van, és az az, amit most küldött be:
    assert len(my_reports) >= 1
    assert my_reports[-1]["watercourse_id"] == "Test River"
