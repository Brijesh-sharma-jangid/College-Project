from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from App.hashing import Hash
from App import schemas, models, database
from App.auth import get_current_user
router = APIRouter(
    prefix = "/user",
    tags=['User']
)

get_db = database.get_db

@router.post('/', response_model = schemas.ShowUser)
def create(request : schemas.User, db : Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password), about_me = request.about_me)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/current', response_model = schemas.ShowUser)
def get_current_user(current_user: schemas.User = Depends(get_current_user), db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user

@router.get('/{id}', response_model = schemas.ShowUser)
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


