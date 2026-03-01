from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import users, reports

# Táblák létrehozása az adatbázisban a models.py alapján
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BISEL API", description="Alap háttérrendszer a BISEL projekthez", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {"message": "Üdvözöl a BISEL projekt webes API-ja! Minden sikeresen elindult!"}
