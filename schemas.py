from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import date

# --- MEASUREMENT SCHEMAS ---
class MeasurementBase(BaseModel):
    type: str
    ref_id: str
    value: str
    unit: Optional[str] = None

class MeasurementCreate(MeasurementBase):
    pass

class Measurement(MeasurementBase):
    id: int
    report_id: int

    model_config = ConfigDict(from_attributes=True)

# --- ENVIRONMENTAL DATA SCHEMAS ---
class EnvironmentalDataBase(BaseModel):
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
    pass

class EnvironmentalData(EnvironmentalDataBase):
    id: int
    report_id: int

    model_config = ConfigDict(from_attributes=True)

# --- REPORT SCHEMAS ---
class ReportBase(BaseModel):
    user_id: Optional[int] = None
    watercourse_id: str
    sampling_site_id: str
    date: date
    quality_class: Optional[str] = None
    bisel_index: Optional[int] = None
    notes: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    environmental_data: Optional[EnvironmentalData] = None
    measurements: List[Measurement] = []

    model_config = ConfigDict(from_attributes=True)

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)
