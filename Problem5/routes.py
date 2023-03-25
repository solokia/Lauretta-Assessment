from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from decorator import check_country_code, get_country_code
from dependencies import get_session
from schemas import UserInterface, Token
import services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix='',
    responses={404: {'description': 'Not found'}}
)

@router.post("/login", response_model=Token)
@check_country_code
def login(request:Request,user: UserInterface, db: Session = Depends(get_session)):
    user = services.authenticate_user(user.username, user.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = services.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
@check_country_code
def create_user(request:Request,user: UserInterface, db: Session = Depends(get_session)):
    try:
        user = services.create_user(user=user, db=db)
    except Exception as e:
        #TODO: redo exception for sql alchemy
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request. User exist")
    return {"id":user.id,"username":user.username}

@router.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    token_data = services.decode_token(token)
    if token_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = services.get_user(token_data.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"id":user.id,"username":user.username}

@router.post("/token/refresh", response_model=Token)
async def refresh_token(token: str = Depends(oauth2_scheme)):
    new_token = services.refresh_token(token)
    if new_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"access_token": new_token, "token_type": "bearer"}