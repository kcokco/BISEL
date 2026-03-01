# BISEL - Projekt Dokumentáció

Ez a dokumentum a BISEL projekt (Python + FastAPI + PostgreSQL webes alkalmazás) lépésről lépésre történő felépítését rögzíti. Kiváló alapként szolgálhat egy LinkedIn bejegyzéshez vagy portfólióhoz.

## 1. Lépés: Projekt alapítás és Virtuális Környezet
* **Cél:** Egy tiszta, izolált fejlesztői környezet létrehozása a projekt számára.
* **Technológia:** Python `venv` (Virtual Environment).
* **Mit csináltunk?**
    1. Létrehoztunk egy új mappát a projektnek: `BISEL`.
    2. Ebben a mappában lefuttattuk a `python -m venv venv` parancsot. Ez létrehozott egy elszigetelt Python környezetet, így a jövőben telepített csomagok (FastAPI, adatbázis illesztők) csak ehhez a projekthez fognak tartozni, és nem okoznak ütközést a rendszer többi részével.

---

## 2. Lépés: Függőségek és csomagok telepítése
* **Cél:** A webes alkalmazáshoz és az adatbázis kezeléshez szükséges Python könyvtárak beszerzése.
* **Technológia:** `pip` (Python csomagkezelő), FastAPI, Uvicorn, SQLAlchemy, psycopg2-binary.
* **Mit csináltunk?**
    1. Aktiváltuk a virtuális környezetet (Windows rendszeren a `.\venv\Scripts\Activate.ps1` parancs kiadásával).
    2. Telepítettük a szükséges csomagokat egyetlen paranccsal: `pip install fastapi uvicorn sqlalchemy psycopg2-binary`.
        * **FastAPI:** A modern, gyors webes keretrendszer az API végpontokhoz.
        * **Uvicorn:** A webszerver, ami a FastAPI alkalmazásunkat fogja futtatni.
        * **SQLAlchemy:** A könyvtár, amivel könnyedén (Python kódként) tudunk beszélgetni az adatbázissal (ezt hívják ORM-nek).
        * **psycopg2-binary:** A konkrét "kártya" (driver), amivel a Python rá tud kapcsolódni a PostgreSQL adatbázisunkra.

---

## 3. Lépés: Az első API végpont és a Web Szerver indítása
* **Cél:** Egy alapvető "Szia Világ" szintű backend készítése, amivel tesztelhetjük, hogy minden telepítés sikeres volt-e.
* **Technológia:** FastAPI, Uvicorn, Python.
* **Mit csináltunk?**
    1. Létrehoztunk egy új fájlt a projekt gyökerében `main.py` névvel.
    2. Ebben írtunk egy minimális FastAPI alkalmazást, ami a gyökér URL-re (`/`) egy visszajelzést ad: `{"message": "Üdvözöl a BISEL projekt webes API-ja! Minden sikeresen elindult!"}`
    3. Elindítottuk a szervert a terminálban: `uvicorn main:app --reload`.
        *  A `--reload` kapcsoló szuper hasznos: minden alkalommal, amikor elmentünk egy fájlt a fejlesztés során, a szerver automatikusan újraindul, így nem kell állandóan leállítani és elindítani.
    4. Ennek eredményeként a szerverünk már mosolyogva fut a [http://127.0.0.1:8000/](http://127.0.0.1:8000/) címen! Ráadásul a FastAPI ingyen és automatikusan ad nekünk egy tesztfelületet is ezen a címen: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 4. Lépés: Adatbázis konfiguráció és Docker konténer indítása
* **Cél:** Egy stabil, szeparált PostgreSQL adatbázis beállítása a fejlesztéshez, és a Python backend csatlakoztatása.
* **Technológia:** Docker Compose, PostgreSQL (15), SQLAlchemy.
* **Mit csináltunk?**
    1. Létrehoztunk egy `docker-compose.yml` fájlt a projekt gyökerében. Ez a fájl mondja meg a Dockernek, hogy indítson el nekünk egy `postgres` nevű konténert a megfelelő jelszóval (`kalligrafia`) és felhasználóval.
    2. A terminálban lefuttattuk a `docker-compose up -d` parancsot. Ez letöltötte (ha még nem volt meg) és a háttérben elindította az adatbázisunkat az 5432-es porton.
    3. Létrehoztunk egy `database.py` nevű fájlt. Ez felelős a Python kód és a Postgres adatbázis közötti híd (engine) kiépítéséért az SQLAlchemy segítségével. A csatlakozási URL-ünk a következő: `postgresql://postgres:kalligrafia@127.0.0.1:5432/postgres`.
    4. Egy gyors teszttel (`python -c "from database import engine; print('SIKERES CSATLAKOZAS' if engine.connect() else 'HIBA')"`) bizonyítottuk, hogy az alkalmazásunk tökéletesen tud kommunikálni az adatbázissal!

---

## 5. Lépés: Adatvalidáció (Schemas) és Adatbázis Műveletek (CRUD)
* **Cél:** A beérkező adatok ellenőrzése Pydantic segítségével, és az adatbázis műveletek (létrehozás, olvasás, stb.) elkülönítése egy külön fájlba a tisztább kód érdekében.
* **Technológia:** Pydantic (FastAPI része), SQLAlchemy.
* **Mit csináltunk?**
    1. Létrehoztunk egy `schemas.py` nevű fájlt. Ebben definiáltuk a Pydantic modelleket, amik leírják, hogy milyen adatokat várunk el a felhasználótól (pl. regisztrációkor `UserCreate`, új mérés leadásakor `ReportCreate`), és miket adunk vissza (`User`, `Report`). Beállítottuk a `from_attributes = True` értéket, hogy az SQLAlchemy adatbázis modellekből könnyen Pydantic objektumokat lehessen csinálni.
    2. Létrehoztunk egy `crud.py` nevű fájlt (Create, Read, Update, Delete). Ide gyűjtöttük össze azokat a Python függvényeket, amik a tényleges adatbázis lekérdezéseket végzik (pl. felhasználó keresése email alapján, új adatsor mentése, adatok lekérdezése). A FastAPI végpontok (routers) később ezeket a függvényeket fogják meghívni.

---

## 6. Lépés: API Végpontok (Routers) Létrehozása
* **Cél:** A korábban megírt adatbázis műveletek (CRUD) elérhetővé tétele a külvilág számára webes végpontokon (HTTP kéréseken) keresztül.
* **Technológia:** FastAPI APIRouter, Dependency Injection.
* **Mit csináltunk?**
    1. Létrehoztunk egy új `routers` nevű mappát, hogy rendszerezetten tartsuk a kódot.
    2. Készítettünk egy `users.py` fájlt a felhasználó kezelés végpontjaihoz (pl. regisztráció `POST /users/`, lekérdezés `GET /users/{id}`). Ezek a végpontok automatikusan meghívják a korábban írt `crud.py` megfelelő metódusait.
    3. Készítettünk egy `reports.py` fájlt a mérések leadásához (`POST /reports/`) és az eddig rögzített listák lekéréséhez (`GET /reports/`).
    4. Módosítottuk a `main.py` főfájlt: sikeresen "olvasztottuk" bele (include\_router) ezt a két új fájlt a fő alkalmazásba.
    5. Beállítottunk egy ún. "Dependency"-t (függőséget) az Adatbázis munkamenetek kezelésére (`get_db`). Ez biztosítja, hogy minden egyes HTTP kérés kapjon egy különálló adatbázis kapcsolatot (sessiont), amit a végén biztonságosan le is zár az alkalmazás.
    6. Az eredmény: ha megnyitjuk a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) linket, már látszanak és azonnal tesztelhetőek a felhasználókat és méréseket kezelő interaktív fejlesztői panelek!

## 7. Lépés: Frontend Inicializálása
* **Cél:** A felhasználói felület (kliens alkalmazás) alapjainak megteremtése egy modern, gyors fejlesztői eszkábával.
* **Technológia:** Node.js, npm, Vite, React (feltételezve a Vite sablont).
* **Mit csináltunk?**
    1. A projekt gyökerében létrehoztunk egy új, `frontend` nevű mappát a Vite segítségével (pl. `npm create vite@latest frontend`).
    2. Ebben a mappában létrejött a kliens alkalmazás alapvza (köztük a `package.json`, `index.html`, `vite.config.js`).
    3. Beállítottuk a szükséges alapfüggőségeket és scripteket a gyors fejlesztéshez és buildeléshez megágyazva a későbbi UI/UX fejlesztéseknek.

## 8. Lépés: Automatikus Backend Tesztelés (Unit & Integrációs)
* **Cél:** Biztosítani az elkészült API végpontok (pl. felhasználók mentése, lekérdezése) hibamentes működését hosszú távon egy robusztus keretrendszerrel, valamint a kimenet megbízható és látványos (HTML) tárolása.
* **Technológia:** `pytest`, `httpx`, FastAPI `TestClient`, `pytest-html`.
* **Mit csináltunk?**
    1. Telepítettük a szükséges tesztelő csomagokat (köztük a HTML riportert is): `pip install pytest httpx pytest-html`.
    2. Létrehoztunk a projekt gyökerében egy `tests` nevű mappát, hogy a tesztkódokat teljesen elkülönítsük az éles alkalmazástól.
    3. Hozzáadtuk az első tesztfájlunkat `test_main.py` néven, benne a `TestClient` példányosításával. Ez azért szuper, mert úgy tudunk teszt lekérdezéseket indítani a backendünk felé mindenféle port nyitás vagy szerver indítás nélkül, mintha igazi kérések lennének.
    4. Megírtunk 2 automatizált ellenőrzést (olvasva és módosítva a dev adatbázist):
        * A gyökér (`/`) API válaszának ellenőrzése.
        * Egy dinamikusan generált email címmel létrehozott tesztfelhasználó sikeres regisztrációja, majd annak visszakeresése (CRUD: Create/Read teszt).
        * A `schemas.py`-ban frissítettük a régi Pydantic lekérdezéseket (`model_config = ConfigDict(from_attributes=True)`), hogy a teszt zöld és *warning* mentes maradjon.
    5. A terminálban sikeresen futtattuk a teszteket úgy, hogy egy emberileg átlátható **HTML jelentést is kigenerált** a rendszer, ami nem vész el a futás után: `pytest tests/test_main.py --html=tests/report.html --self-contained-html` parancs kiadásával.

---

*(További lépések hamarosan...)*
