from fastapi import APIRouter, Depends, HTTPException, status
from App import schemas, database, models, token
from sqlalchemy.orm import Session
from App.hashing import Hash
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags = ['Login']
)

get_db = database.get_db

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post('/login')
def login(request:schemas.Login, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="incorrect password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}