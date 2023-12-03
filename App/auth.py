from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from App import models, database

from . import token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

get_db = database.get_db
db : Session = Depends(get_db)

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = token.token_verify(data, credentials_exception)
    return token_data

    
