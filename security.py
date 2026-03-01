from passlib.context import CryptContext

# Bcrypt titkosító kontextus beállítása
# A "deprecated='auto'" biztosítja, hogy automatikusan kezelje az elavult hash-eket a jövőben
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Összehasonlít egy nyers jelszót (pl. amit a felhasználó beírt) 
    az adatbázisban tárolt bcrypt hash-el.
    Visszatérési érték: True, ha egyeznek, különben False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Vesz egy tiszta szöveges jelszót és bcrypt segítségével 
    egy biztonságos, sót (salt) tartalmazó hash-t generál belőle.
    Ezt az értéket kell elmenteni az adatbázisba.
    """
    return pwd_context.hash(password)
