from typing import List, Union
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name : str
    email : str
    password: str
    about_me : str = None

class ShowUser(BaseModel):
    id : int
    name : str
    email : str
    about_me : str = None
    password : str

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None

class Tag(BaseModel):
    tag_word : str

class TagCreate(Tag):
    pass

class QuestionBase(BaseModel):
    title: str
    ques_content: str

class QuestionCreate(QuestionBase):
    tags: List[Tag] = []

class QuestionUpdate(QuestionBase):
    tags: List[Tag] = []

class QuestionShow(QuestionBase):
    id: int
    views: int = 1
    is_answered: bool = False
    votes: int = 0
    has_acceptable_answer: bool = False
    user_id: int
    tags: List[Tag] = []
    class Config:
        orm_mode = True



class AnswerBase(BaseModel):
    ans_content: str

class AnswerCreate(AnswerBase):
    pass

class AnswerShow(AnswerBase):
    id: int
    question_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    

