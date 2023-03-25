from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from models import User
from passlib.context import CryptContext
from schemas import UserInterface, TokenData
from sqlalchemy.orm.session import Session

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

hash_helper = CryptContext(schemes=["bcrypt"])

def create_user(user: UserInterface, db:Session):
    hashed_password = hash_helper.hash(user.password)
    user = User(username=user.username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(username: str,db:Session):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(username: str, password: str, db:Session):
    user = get_user(username, db)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        return token_data
    except jwt.JWTError:
        return None

def refresh_token(token: str):
    token_data = decode_token(token)
    if token_data:
        new_token = create_access_token(data={"sub": token_data.username})
        return new_token
    return None
