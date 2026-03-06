from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt

# Token Configurations
SECRET_KEY = "bisel-super-secret-jwt-key-change-it-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Bcrypt titkosító kontextus beállítása
# A "deprecated='auto'" biztosítja, hogy automatikusan kezelje az elavult hash-eket a jövőben
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Összehasonlít egy nyers jelszót (pl. amit a felhasználó beírt) 
    az adatbázisban tárolt bcrypt hash-el.
    Visszatérési érték: True, ha egyeznek, különben False.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        # Ha az adatbázisban régi, nem bcrypt-tel titkosított jelszó van
        return False

def get_password_hash(password: str) -> str:
    """
    Vesz egy tiszta szöveges jelszót és bcrypt segítségével 
    egy biztonságos, sót (salt) tartalmazó hash-t generál belőle.
    Ezt az értéket kell elmenteni az adatbázisba.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Egy szótárnyi adatot (pl. felhasználó azonosító) kódol le JWT tokenné.
    Hozzáadja a lejárati időt.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
