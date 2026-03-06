from sqlalchemy.orm import Session
import models
import schemas
import security

# -----------------------------------------------------------------------------
# USER CRUD (Felhasználók kezelése)
# Ez a blokk tartalmazza azokat a függvényeket, amik a felhasználókkal
# kapcsolatos adatbázis műveletekért (pl. keresés, létrehozás) felelnek.
# -----------------------------------------------------------------------------

def get_user(db: Session, user_id: int):
    """Lekérdez egyetlen felhasználót az egyedi azonosítója (ID) alapján."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Megkeres egy felhasználót az email címe alapján.
    Hasznos a bejelentkezésnél vagy regisztrációnál (van-e már ilyen email).
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Új felhasználót hoz létre az adatbázisban a kapott adatok (Pydantic schema) alapján.
    Figyelem: Jelenleg a jelszó "ál-hashelt", élesben bcrypt könyvtárra lesz szükség!
    
    """
    # Jelszó titkosítása valódi biztonsági algoritmussal (Bcrypt)
    hashed_password = security.get_password_hash(user.password)
    
    # 1. Példányosítjuk az SQLAlchemy User modellt
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    
    # 2. Hozzáadjuk a session-höz (a "bevásárlókosárhoz")
    db.add(db_user)
    # 3. Véglegesítjük (elmentjük) a tranzakciót az adatbázisban
    db.commit()
    # 4. Frissítjük a példányt az adatbázis által generált adatokkal (pl. ID)
    db.refresh(db_user)
    
    return db_user

# -----------------------------------------------------------------------------
# REPORT CRUD (Mérések és Riportok kezelése)
# Ezek a függvények felelnek a biológiai mérések, riportok és a hozzájuk 
# tartozó környezeti adatok adatbázisba mentéséért és listázásáért.
# -----------------------------------------------------------------------------

def get_reports(db: Session, skip: int = 0, limit: int = 100):
    """
    Lekérdezi az összes rögzített mérést (riportot) az adatbázisból.
    Lapozás (pagination) támogatott a `skip` és `limit` paraméterekkel.
    """
    return db.query(models.Report).offset(skip).limit(limit).all()

def get_reports_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Lekérdezi az egy adott felhasználóhoz tartozó méréseket."""
    return db.query(models.Report).filter(models.Report.user_id == user_id).offset(skip).limit(limit).all()

def create_report(db: Session, report: schemas.ReportCreate):
    """Új fő riport rekord (pl. horgász vagy biológus mérése) létrehozása."""
    # A **report.model_dump() a pydantic validált adatokat adja át a modellnek "kicsomagolva"
    db_report = models.Report(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def create_report_environmental_data(db: Session, env_data: schemas.EnvironmentalDataCreate, report_id: int):
    """
    A fő riporthoz tartozó környezeti adatok (vízhőmérséklet, időjárás stb.) lementése 
    egy különálló táblába. Összekapcsolva a report_id alapján.
    """
    db_env_data = models.EnvironmentalData(**env_data.model_dump(), report_id=report_id)
    db.add(db_env_data)
    db.commit()
    db.refresh(db_env_data)
    return db_env_data

def create_report_measurement(db: Session, measurement: schemas.MeasurementCreate, report_id: int):
    """
    Egy konkrét mért adat (pl. egy meghatározott rovarfaj egyedszáma) lementése.
    Ebből több is tartozhat egyetlen fő riporthoz (report_id).
    """
    db_measurement = models.Measurement(**measurement.model_dump(), report_id=report_id)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement
