from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal
from routers.users import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Report)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """Új jelentés beküldése, automatikusan a bejelentkezett felhasználóhoz (user_id) rendelve."""
    report.user_id = current_user.id
    return crud.create_report(db=db, report=report)

@router.get("/", response_model=List[schemas.Report])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Végpont az összes jelentés lekérdezéséhez (publikus)."""
    reports = crud.get_reports(db, skip=skip, limit=limit)
    return reports

@router.get("/me", response_model=List[schemas.Report])
def read_my_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """Végpont a bejelentkezett felhasználó saját jelentéseinek lekérdezéséhez."""
    reports = crud.get_reports_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return reports
