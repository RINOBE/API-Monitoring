from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from schemas import Token,TokenData
from databases import SessionLocal, engine,get_db
from models import User
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter,Request,WebSocket
import time

router = APIRouter()

SECRET_KEY = "mkdfjdlkfjodifjodigj90493R04RFFD%§oeifjzeofi984345029RIFJDFDIFJ43JFKDFKSD23"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2340

class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None):
        return await super().__call__(request or websocket)
oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Vérifiez si le token a expiré
    if payload.get("exp") is None or payload["exp"] < time.time():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Le token a expiré")

    return token_data

def get_password_hash(password):
    return pwd_context.hash(password)
