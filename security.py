from fastapi.security import OAuth2PasswordBearer
from models import TokenData
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta
import database
from passlib.context import CryptContext
from decouple import config



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/vets/login")


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password):
    return password_context.hash(password)

async def get_current_vet(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ne mogu provjeriti autentifikacijske podatke",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    vet = await database.fetch_vet(username=token_data.username)
    if vet is None:
        raise credentials_exception
    return vet

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=45)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_vet(username: str, password: str):
    print("Inside authenticate_vet function")  
    
    vet = await database.fetch_vet(username)
    if not vet:
        return False
    if not verify_password(password, vet["hashed_password"]):
        return False
    print(f"Object being returned: {vet}, Type: {type(vet)}")  

    return vet





