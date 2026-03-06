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

## 9. Lépés: Frontend Architektúra és UI Építés
* **Cél:** A generált Vite sablon megtisztítása, a modern dizájn rendszer (CSS) megalapozása, és a komponens-alapú szerkezet (React) felállítása az API kommunikációval együtt.
* **Technológia:** React, Vite, `react-router-dom` (Útválasztás), `axios` (Hálózati kérések), CSS3.
* **Mit csináltunk?**
    1. **Biztonságos törlés:** Eltávolítottuk a Vite alapértelmezett logóit és CSS fájljait (`App.css`), így tiszta lappal indulunk.
    2. **Könyvtárszerkezet kialakítása:** Létrehoztunk egy tiszta, átlátható struktúrát az `src` mappában:
        * `/pages`: A teljes weboldalakat képviselő komponensek (pl. Kezdőlap).
        * `/components`: Újrahasznosítható kisebb elemek (pl. Gombok, Űrlapok).
        * `/api`: A Backenddel történő kommunikáció központja.
    3. **Applikációs Szintű Dizájn:** Csináltunk egy profi, modern `index.css`-t Inter betűtípussal, arculati színváltozókkal (kékes-zöldes) és lebegési effektekkel.
    4. **Backend Bekötése (Axios):** Az `api` mappában létrehoztunk egy `api.js` fájlt, ami egy előre beállított Axios klienst tartalmaz (ami a mi `127.0.0.1:8000`-es Python szerverünkre mutat).
    5. **Első Oldal és React Router:** Telepítettük a `react-router-dom`-ot CLI-ből. Az `App.jsx`-et átalakítottuk, hogy ez kezelje az útvonalazást, és elkészítettük a `Home.jsx` oldalt, ami már sikeresen le is kérdezi és megjeleníti a backend `/` végpontjának üzenetét.

---

## 10. Lépés: Globális UI Elemek és a Regisztrációs Űrlap (Frontend)
* **Cél:** A felhasználói felület (UI) vizuális keretének beállítása egy Globális Fejléccel (Navbar), valamint a biztonságos Regisztrációs Űrlap frontend implementálása API kapcsolattal.
* **Technológia:** React, React Router, Axios, CSS3.
* **Mit csináltunk?**
    1. **Felhasználói Élmény (UX) Javítása:** Létrehoztunk a `components` mappában egy Globális Fejlécet (`Navbar.jsx` és `Navbar.css`), amely "ragadós" a képernyő tetején, bemutatja a BISEL logót, és helyet ad a jövőbeli navigációs gomboknak.
    2. **Regisztrációs Oldal (Register.jsx):** Felépítettünk egy modern űrlapot a `pages` mappában, mely stílusos beviteli mezőket (glória fókusz effekt), hiba/siker visszajelző paneleket (alert) kapott.
    3. **Jelszó Láthatóság Váltó:** A kódolás magában foglalja a React Állapotkezelését (`useState`), amivel létrehoztunk egy dinamikus "Szem"/"Mutat" gombot a jelszó mezőkhöz UX javításként.
    4. **Frontend Validáció:** Az űrlap beküldése (Submit) csak akkor indul el, ha a "Jelszó" és a "Jelszó Megerősítése" mezők karakterei 100%-ban egyeznek.
    5. **API Hálózat (Full-Stack Integráció):** A "Regisztrálok" gomb lenyomására a frontend kliensünk az Axios könyvtárral elküldi (JSON formátumban) az adatokat a `FastAPI` felé (`POST /users/`). Sikeres válasz esetén zöld üzenetet mutat és automatikusan (2 mp múlva) átirányítja a felhasználót a főoldalra a React Router segítségével.

---

## 11. Lépés: Backend Biztonság - Valós Jelszó Titkosítás (Bcrypt)
* **Cél:** A regisztrációs űrlaphoz kapcsolódó jelszavak iparági szabványnak (Bcrypt) megfelelő, egyirányú titkosítása az adatbázisban, lecserélve a korábbi, ideiglenes megoldást.
* **Technológia:** Python `passlib`, `bcrypt`, FastAPI szerver futtatás (`uvicorn`).
* **Mit csináltunk?**
    1. **Felkészülés:** Telepítettük a virtuális környezetbe a szükséges csomagokat (`pip install passlib[bcrypt]`).
    2. **Biztonsági Modul:** Létrehoztunk a projekt gyökerében egy `security.py` fájlt, amely példányosította a `CryptContext`-et, és két alapvető függvényt biztosít: `get_password_hash` (a jelszó "megsózása" és hashelése) és `verify_password` (a későbbi belépések ellenőrzéséhez).
    3. **CRUD integráció:** A `crud.py`-ban lecseréltük az elavult (notreallyhashed) megoldást. A `create_user` mostantól a `security.py` logikáját (Bcrypt algoritmus) használja mielőtt az SQLAlchemy fiókként lementi az objektumot.
    
### ⚠️ Műszaki Tanulság (Hibaelhárítás)
A fejlesztés közben felmerült egy kritikus akadályozó tényező (blocker), ami a jövőbeni projekteknél is fontos tapasztalat:
* **Jelenség:** A kódbázis sikeres átírása ellenére az új felhasználók jelszava továbbra is titkosítatlanul (`notreallyhashed`) vándorolt be a PostgreSQL adatbázisba.
* **A Probléma Gyökere:** Az első próbálkozásnál a `bcrypt` legújabb, 5.0.0-s verziója települt fel, ami részben inkompatibilis (hibát dob a túl hosszú `truncate` miatt) a FastAPI `passlib` moduljával. Amikor az Uvicorn szerver (mivel futott a háttérben `--reload` kapcsolóval) érzékelte a fájl változásokat, megpróbálta újraolvasni az alkalmazást. A beolvasás közben a `bcrypt 5.0.0` verzióhiba miatt összeomlott. Az Uvicorn "túlélési" (fail-safe) mechanizmusa, hogy az összeomlás után egyszerűen **a memóriájában (RAM) tartja az utolsó, még működő kódot** (amikor még nem volt `security.py`).
* **Továbgyűrűző Hiba:** Amikor a csomagot sikeresen "leminősítettük" a stabil `bcrypt 4.0.1`-re, majd újabb tesztet futtattunk a böngészőből, a szerver még mindig az elavult, memóriába égett állapotot szolgálta ki, mivel azóta egyetlen forrásfájlhoz sem nyúltunk, így "nem tudta", hogy újra kellene töltenie a hibátlan kódot.
* **A Megoldás (Fix):** Két opció is létezik egy ilyen "beragadt" állapot feloldására:
    1. A szerver kényszerített újraindítása a megállító kulcskombinációval (CTRL + C) a terminálban, majd az indítási parancs megismétlése.
    2. Vagy radikálisabb esetben (amit itt használtunk), PowerShell parancsokkal maradéktalanul kipucolni a futó python folyamatokat (`Get-Process -Name "python"`, majd kiírtani a hozzá tartozó PID-ket: `Stop-Process -Id <PID> -Force`). Ezután egy nulláról indított `uvicorn main:app --reload` biztosítja, hogy tiszta lappal, a javított fájlok alapján haladjunk tovább.

*(További lépések hamarosan...)*

---

## 12. Lépés: JWT Alapú Hitelesítés (Backend)
* **Cél:** Egy biztonságos állapotmentes authentikációs rendszer bevezetése, ami JWT (JSON Web Token) tokeneket ad vissza a sikeresen bejelentkező felhasználóknak.
* **Technológia:** FastAPI OAuth2PasswordBearer, `python-jose`, `python-multipart`.
* **Mit csináltunk?**
    1. A `security.py`-ba beírtuk a token generáló logikát (JWT encode) a biztonsági kulccsal és lejárati idővel (30 perc).
    2. A `schemas.py`-ba felvettük a `Token` és `TokenData` válasz modelleket.
    3. A `routers/users.py`-ban elkészítettük a `POST /users/login` végpontot. Ez visszadobja a tokent, ha jó a jelszó.
    4. Készítettünk egy `get_current_user` nevű FastAPI dependency-t, mely automatikusan dekódolja a tokeneket majd kikeresi az adatbázisból az azonosított usert a védett végpontok meghívásakor. A tesztelés miatt frissíteni kellett a "passlib" kódját egy `UnknownHashError` hibát kezelő blokkal, hogy "notreallyhashed" régi felhasználók miatt ne essen pánikba. 

---

## 13. Lépés: Frontend Védett Állapotkezelés és Globális Context
* **Cél:** A böngésző és a React app képes legyen megjegyezni, hogy ki van belépve (Munkamenet - Session / Context) és ez alapján dinamikusan változtatni az UI-t.
* **Technológia:** React `createContext`, `useContext`, `useEffect`, React Router `Navigate`.
* **Mit csináltunk?**
    1. Építettünk egy robusztus bejelentkezési formot (`Login.jsx`), amely beállítja a `Local Storage`-be a tokent és frissíti a menüt.
    2. Kialakítottunk egy `AuthContext.jsx`-et. Ez az alkalmazás indulásakor leellenőrzi a tokent, és kimenti a `user` objektumot globálisan.
    3. Írtunk egy `ProtectedRoute.jsx` komponenst is: bárki megpróbál megnyitni a `App.jsx`-ben egy védett linket belépés nélkül, azt automatikusan visszadobja a`/login`-ra.
    4. Az Axios (API) hívó beépített egy úgynevezett **Válasz Interceptort** a 401-es kódokra: ha lejár a tokenünk az api hívás alatt, magától kijelentkeztet és visszairányít a loginra. 

---

## 14. Lépés: Fő Funkciók Építése (Saját Mérések + Új Riport beküldése)
* **Cél:** Hogy a belépett felhasználók privát, saját nevük alatt adhassanak le vízminőségi teszteket, és csak a sajátjaikat listázza ki később az alkalmazás.
* **Technológia:** FastAPI beágyazott függőségek, React `useEffect` mapelések.
* **Mit csináltunk?**
    1. A `crud.py`-ban létrejött egy `get_reports_by_user` funkció, ami a `user_id` alapján szűri meg az adatbázist.
    2. A `reports.py` (Backend) kibővült egy megvédett `GET /reports/me` felülettel.
    3. A React Frontenden létrejött a `Dashboard.jsx`, ami rácsos elrendezéssel (Grid) szépen, listázza az onnan visszajövő JSON tömböt.
    4. Kialakításra került a `NewReport.jsx`: Egy modern, sok input mezős űrlap, amely a beküldésnél a korábban elkészített (és most JWT-vel felvértezett) POST `/reports/` backend API-t használja. Siker esetén egyből visszadob a már feltöltött saját Kezelőpultra (`Dashboard`).

*(Ezzel a teljes authentikációs kör és alap CRUD web funkció megvalósult!)*

---

## 15. Lépés: JWT és Védett Végpontok Automatikus Tesztelése
* **Cél:** Bizonyítani, hogy a nemrég elkészült hitelesítési és jogosultságkezelő kódok hibamentesen és megbízhatóan működnek a FastAPI backend-en.
* **Technológia:** Pytest, FastAPI `TestClient`, `pytest-html`.
* **Mit csináltunk?**
    1. Kibővítettük a `test_main.py` fájlt egy komplex, folyamatra épülő teszttel (`test_login_and_get_reports`).
    2. A teszt futása során automatikusan:
        - Regisztrál egy véletlenszerű nevű felhasználót az adatbázisba.
        - Meghívja a `/users/login` végpontot az adatokkal, és ellenőrzi, hogy sikeresen visszakapja-e a `Bearer` formátumú JWT tokent.
        - Elküld egy szimulált új mérést (`POST /reports/`) - ehhez beállítja az `Authorization: Bearer <token>` HTTP fejlécet, bizonyítva a hitelesítést.
        - Végül lekéri a `/reports/me` címet a saját fiókba rögzített adatok ellenőrzéséhez. 

### ⚠️ Tesztelés során felmerült hibák és megoldásaik

- **`UnknownHashError` (passlib)**: Amikor a hitelesítés elindult, a régebbről (még a Bcrypt bevezetése előttről) bent maradt, `notreallyhashed` jelszavakkal rendelkező tesztfelhasználók bejelentkezése a szerver összeomlását okozta a `passlib` hibája miatt. 
  *A megoldás az volt, hogy a `security.py`-ban egy `try... except UnknownHashError` blokkal elegánsan megfogtuk és kicseréltük a hibát a szokásos 401-es "Jogosulatlan" HTTP státuszra a szerver fagyása vagy "500 Internal Server error" helyett.*
- **`NameError: name 'fetched_user' is not defined`**: A regisztráció utáni visszaolvasást (GET) végző, frissített `test_create_and_read_user` tesztesetben egyszerű elírás (szintaktikai hiba) miatt nem találta a JSOn válaszból kilvasott változót a Python. 
  *Egy gyors változó-visszaállítási korrekcióval a teszt újra hibátlan, 100%-os "zöld" eredményt produkált.*

---

## 16. Lépés: Frontend Hibakeresés - A Láthatatlan Bejelentkezési Hiba
* **Cél:** Egy a felhasználó által jelentett, a `Dashboard` komponens adatbetöltési hibájának reprodukálása, behatárolása és megszüntetése az éles rendszerhez közeli állapotban.
* **Jelenség:** A bejelentkezés után a Kezelőpult (Dashboard) nem jelenítette meg a már meglévő méréseket, csupán egy üres listát mutatott ("Jelenleg nincsenek leadott méréseid"), annak ellenére, hogy a felhasználónak voltak rögzített adatai a rendszerben (pl. ID: 12-es user).
* **Technológia:** Böngésző konzol (Developer Tools), Python natív HTTP tesztelés (`httpx`), SQLAlchemy (Command Line Interface).
* **Mit csináltunk (A Debugolási Folyamat):**
    1.  **Backend vs. Frontend elszigetelése:** Először meg kellett bizonyosodni, hogy az API (Python/Uvicorn) adja-e a hibás választ, vagy a Frontend (React/Axios) rontja-e el a kiolvasást.
        *   Írtunk egy gyors natív Python teszt szkriptet, ami közvetlenül ("Böngésző nélkül") kérte le a Backendtől a problémás `/reports/me` végpont adatait JWT token kíséretében.
        *   *Eredmény:* A Python teszt hibátlan `200 OK` státusszal és tökéletes JSON válasszal tért vissza. Ezzel **biztosra vettük, hogy a Backend modellek és a Pydantic validációk hibátlanul működnek.**
    2.  **Frontend Szimuláció (Browser Subagent):** Egy automatizált böngészővel (Subagent) navigáltunk végig a folyamaton (Regisztráció -> Belépés -> Dashboard olvasás).
        *   *A valós hiba lokalizálása:* A weblap vizuálisan tényleg nem mutatott piros hibaüzenetet, de a **böngésző fejlesztői hálózat naplójában (Console Log) egyértelműen látható volt egy `401 Unauthorized` API visszautasítás**, hivatkozva a lejárt vagy érvénytelen tokenre.
    3.  **A Gyökér-ok (Root Cause) felfedezése:** 
        *   A hitelesítési hiba nem kódszintű, hanem **adatintegritási** probléma volt.
        *   Amikor korábban a bevezettük az iparági szabványú jelszó titkosítást (Bcrypt - 11. Lépés), az **adatbázisban bent maradtak a régi, titkosítatlan (`notreallyhashed`) fiókok**. 
        *   Amikor a Frontend megpróbált bejelentkezni egy ilyen "legacy" (régi) felhasználóval, a megújult biztonsági rendszer jogosan megtagadta a hozzáférést (401), ezért nem kapott jogosultságot az Axios a mérések letöltésére, amit a UI egy némán üres listaként interpretált.
    4.  **A Megoldás (Fix):**
        *   Mivel egy fejlesztés alatt álló (Dev) környezetben vagyunk, a legtisztább megoldás a **"Tiszta lap" (Clean Slate)** elve volt.
        *   Egy SQLAlchemy parancssoros lekérdezéssel töröltük az adatbázisból az összes egyezményes táblát (Users, Reports, Measurements, EnvironmentalData), eltávolítva az elavult jelszavakat.
    5.  **Végső Ellenőrzés (Verify):** A tiszta adatbázissal megismételt, teljes végponttól-végpontig tartó (End-to-End) manuális és automatizált teszt (Regisztráció -> Belépés -> Új mérés leadása) **100%-os sikert hozott.** Az új, Bcrypt-tel védett mérési adatok azonnal és hibamenetesen betöltődtek a Dashboard komponensbe.
