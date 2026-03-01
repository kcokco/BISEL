from sqlalchemy.orm import Session
import models, schemas

# --- USER CRUD ---

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Dummy "hash" for now, we will add proper hashing later if needed
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, name=user.name, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- REPORT CRUD ---

def get_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Report).offset(skip).limit(limit).all()

def create_report(db: Session, report: schemas.ReportCreate):
    db_report = models.Report(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def create_report_environmental_data(db: Session, env_data: schemas.EnvironmentalDataCreate, report_id: int):
    db_env_data = models.EnvironmentalData(**env_data.model_dump(), report_id=report_id)
    db.add(db_env_data)
    db.commit()
    db.refresh(db_env_data)
    return db_env_data

def create_report_measurement(db: Session, measurement: schemas.MeasurementCreate, report_id: int):
    db_measurement = models.Measurement(**measurement.model_dump(), report_id=report_id)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement
