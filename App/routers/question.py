from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from App.models import Question, User, Tag, QuestionTag, UserVote
from typing import List
from App.database import get_db
from App.schemas import QuestionShow, QuestionCreate, TagCreate, QuestionUpdate
from App import schemas
from App.auth import get_current_user

router = APIRouter(
    tags = ['Question']
)



@router.post("/", response_model=QuestionShow)
def create_question(
    question: QuestionCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Create question
    user = db.query(User).filter(User.email == current_user.email).first()
    new_question = Question(**question.dict(exclude={'tags'}), user_id=user.id)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    tags = []
    # Handle tags
    for tag in question.tags:
        db_tag = db.query(Tag).filter(Tag.tag_word == tag.tag_word).first()
        if db_tag is None:
            db_tag = Tag(**tag.dict())
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
        question_tag = QuestionTag(question_id=new_question.id, tag_id=db_tag.id)
        db.add(question_tag)
        tags.append(schemas.Tag(tag_word=db_tag.tag_word))

    db.commit()
    db.refresh(new_question)

    return QuestionShow(**new_question.__dict__, tags=tags)



@router.get("/questions/{question_id}", response_model=QuestionShow)
def read_question(question_id: int, db: Session = Depends(get_db)):

    question_tags = db.query(QuestionTag).filter(QuestionTag.question_id == question_id).all()
    if not question_tags:
        raise HTTPException(status_code=404, detail="Question not found")

    tags = [schemas.Tag(tag_word=question_tag.tag.tag_word) for question_tag in question_tags]

    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question.views += 1
    db.commit()
    db.refresh(question)
    
    question_with_tags = QuestionShow(**question.__dict__, tags=tags)

    return question_with_tags


@router.get("/questions", response_model=List[QuestionShow])
def read_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return [QuestionShow(**q.__dict__, tags = [schemas.Tag(tag_word=tag.tag.tag_word) for tag in db.query(QuestionTag).filter(QuestionTag.question_id == q.id).all()]) for q in questions] 

@router.put("/questions/{question_id}", response_model=QuestionShow)
def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user.email).first()
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    if db_question.user_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to update this question")

    # Update question fields
    for key, value in question_update.dict(exclude={'tags'}).items():
        setattr(db_question, key, value)

    db.query(QuestionTag).filter(QuestionTag.question_id == question_id).delete()

    tags = []
    for tag in question_update.tags:
        db_tag = db.query(Tag).filter(Tag.tag_word == tag.tag_word).first()
        if db_tag is None:
            db_tag = Tag(**tag.dict())
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
        question_tag = QuestionTag(question_id=question_id, tag_id=db_tag.id)
        db.add(question_tag)
        tags.append(schemas.Tag(tag_word=db_tag.tag_word))

    db.commit()
    db.refresh(db_question)

    return QuestionShow(**db_question.__dict__, tags=tags)

@router.delete("/questions/{question_id}", response_model=dict)
def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user.email).first()
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    if db_question.user_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this question")

    db.query(QuestionTag).filter(QuestionTag.question_id == question_id).delete()
    db.delete(db_question)
    db.commit()

    return {"message": "Question deleted successfully"}

@router.post("/questions/{question_id}/vote")
def upvote_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    id = db.query(User).filter(User.email == current_user.email).first().id
    existing_vote = db.query(UserVote).filter(
        UserVote.user_id == id,
        UserVote.question_id == question_id
    ).first()
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    ok = 0
    if existing_vote:
        question.votes -= 1
        db.delete(existing_vote)
        ok = 1
    else:
        question.votes += 1
        db.add(UserVote(user_id=id, question_id=question_id))

    msg = "Question upvoted successfully"
    if ok:
        msg = "Question Downvoted successfully"
    db.commit()
    return {"message": msg}




