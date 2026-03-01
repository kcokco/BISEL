from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="client")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Jövőbeli login-hoz opcionális egyelőre
    watercourse_id = Column(String, index=True)
    sampling_site_id = Column(String)
    date = Column(Date)
    quality_class = Column(String, nullable=True)
    bisel_index = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    
    environmental_data = relationship("EnvironmentalData", back_populates="report", uselist=False)
    measurements = relationship("Measurement", back_populates="report")
    user = relationship("User")

class EnvironmentalData(Base):
    __tablename__ = "environmental_data"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"))
    weather_condition = Column(String, nullable=True)
    air_temp = Column(Float, nullable=True)
    precipitation = Column(String, nullable=True)
    wind_dir = Column(String, nullable=True)
    wind_speed = Column(Float, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    water_level = Column(String, nullable=True)
    flow_rate = Column(String, nullable=True)
    substrate = Column(JSON, nullable=True) 
    riparian_vegetation = Column(String, nullable=True)
    visibility = Column(String, nullable=True)
    access_notes = Column(String, nullable=True)
    observers = Column(JSON, nullable=True) 
    
    report = relationship("Report", back_populates="environmental_data")

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"))
    type = Column(String, index=True) # CHEMICAL vagy TAXON
    ref_id = Column(String, index=True)
    value = Column(String) # Stringet használunk, mert lehet szám (3.4) és minőségi érték ("barna") is.
    unit = Column(String, nullable=True)
    
    report = relationship("Report", back_populates="measurements")
