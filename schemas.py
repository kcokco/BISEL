from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional, List, Any, Dict
from datetime import date

# --- MEASUREMENT SCHEMAS ---
class MeasurementBase(BaseModel):
    """Közös alap egyetlen mérés/megfigyelés (kémiai vagy taxon) adataihoz."""
    type: str
    ref_id: str
    value: str
    unit: Optional[str] = None

class MeasurementCreate(MeasurementBase):
    """Mérés létrehozásakor (POST) várt adatok, megegyezik az alappal."""
    pass

class Measurement(MeasurementBase):
    """Adatbázisból visszatérő mérés modell (válaszhoz), ID-val és a riport hivatkozással kiegészítve."""
    id: int
    report_id: int

    model_config = ConfigDict(from_attributes=True)

# --- ENVIRONMENTAL DATA SCHEMAS ---
class EnvironmentalDataBase(BaseModel):
    """Közös alap a környezeti/fizikai paraméterekhez (pl. időjárás, vízállás)."""
    weather_condition: Optional[str] = None
    air_temp: Optional[float] = None
    precipitation: Optional[str] = None
    wind_dir: Optional[str] = None
    wind_speed: Optional[float] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    water_level: Optional[str] = None
    flow_rate: Optional[str] = None
    substrate: Optional[Any] = None # JSON
    riparian_vegetation: Optional[str] = None
    visibility: Optional[str] = None
    access_notes: Optional[str] = None
    observers: Optional[Any] = None # JSON

class EnvironmentalDataCreate(EnvironmentalDataBase):
    """Környezeti adatok rögzítésekor várt struktúra."""
    pass

class EnvironmentalData(EnvironmentalDataBase):
    """Adatbázisból visszatérő környezeti adatok az azonosítókkal kiegészítve."""
    id: int
    report_id: int

    model_config = ConfigDict(from_attributes=True)

# --- REPORT SCHEMAS ---
class ReportBase(BaseModel):
    """Egy vízminőségi riport (mérés helye, ideje, eredménye) közös alapadatai."""
    user_id: Optional[int] = None
    watercourse_id: str
    sampling_site_id: str
    date: date
    quality_class: Optional[str] = None
    bisel_index: Optional[int] = None
    notes: Optional[str] = None

class ReportCreate(ReportBase):
    """Új riport beküldésekor (POST) a klienstől várt JSON struktúra."""
    @field_validator('date')
    @classmethod
    def date_must_not_be_in_future(cls, v):
        if v > date.today():
            raise ValueError('A mérés dátuma nem lehet a jövőben.')
        return v

class Report(ReportBase):
    """A teljes riport válasz modellje, ami már tartalmazza a beágyazott mérési és környezeti adatokat is."""
    id: int
    environmental_data: Optional[EnvironmentalData] = None
    measurements: List[Measurement] = []

    model_config = ConfigDict(from_attributes=True)

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    """A felhasználói adatok közös alapjai (név, email)."""
    name: Optional[str] = None
    email: EmailStr

class UserCreate(UserBase):
    """Regisztrációnál (POST) várt adatok, ami kötelezően kiegészül a jelszóval."""
    password: str

class User(UserBase):
    """Válaszban visszatérő felhasználói profil. A jelszót soha nem küldjük vissza!"""
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)

# --- AUTH SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
