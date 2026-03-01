from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# A kapott PostgreSQL csatlakozási URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:kalligrafia@127.0.0.1:5432/postgres"

# Az 'engine' a fő belépési pont az adatbázis felé
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# A 'SessionLocal' egy adatbázis munkamenet gyár, amivel később lekérdezéseket indíthatunk
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A 'Base' osztályból fognak öröklődni az adatbázis tábláinkat leíró Python osztályok
Base = declarative_base()
