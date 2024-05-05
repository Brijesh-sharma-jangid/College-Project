from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from App.models import Question, User, Tag, QuestionTag, Answer
from typing import List
from App.database import get_db
from App.schemas import AnswerCreate, AnswerShow
from App import schemas
from App.auth import get_current_user

router = APIRouter(
    tags = ['Answer']
)

@router.post("/questions/{question_id}/answers/", response_model=AnswerShow)
def create_answer_for_question(question_id: int, answer: AnswerCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    new_answer = Answer(**answer.dict(), question_id=question_id, user_id=user.id)
    user.ans_given += 1
    db.commit()
    db.refresh(user)

    question = db.query(Question).filter(Question.id == question_id).first()
    question.answered = True
    db.commit()
    db.refresh(question)

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return new_answer

# Retreive all answer for particular question
@router.get("/questions/{question_id}/answers/", response_model=List[AnswerShow])
def read_answer_for_question(question_id: int, db: Session = Depends(get_db)):

    answer = db.query(Answer).filter(Answer.question_id == question_id)
    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")

    return answer

# Retreive answer for particular user on a question
@router.get("/questions/{question_id}/user/answer/", response_model=AnswerShow)
def read_answer_for_question_for_user(question_id: int,current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == current_user.email).first()
    answer = db.query(Answer).filter(Answer.question_id == question_id, Answer.user_id == user.id).first()
    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")

    return answer

@router.delete("/questions/{question_id}/answers/{answer_id}", response_model=AnswerShow)
def delete_answer_for_question(question_id: int, answer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    db_answer = db.query(Answer).filter(Answer.id == answer_id, Answer.question_id == question_id, Answer.user_id == user.id).first()
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    user.ans_given -= 1
    db.delete(db_answer)
    db.commit()

    return db_answer

@router.put("/questions/{question_id}/answers/{answer_id}", response_model=AnswerShow)
def update_answer_for_question(question_id: int, answer_id: int, answer: AnswerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    db_answer = db.query(Answer).filter(Answer.id == answer_id, Answer.question_id == question_id, Answer.user_id == user.id).first()
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")

    for key, value in answer.dict().items():
        setattr(db_answer, key, value)

    db.commit()
    db.refresh(db_answer)

    return db_answer

