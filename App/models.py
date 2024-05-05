from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from App.database import Base

class UserVote(Base):
    __tablename__ = "user_votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)

    user = relationship("User", back_populates="Votes")
    question = relationship("Question", back_populates="Votes")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    about_me = Column(String, nullable=True)
    ans_given = Column(Integer, default=0)
    password = Column(String)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())

    Votes = relationship("UserVote", back_populates="user")
    questions = relationship("Question", back_populates="user")
    answers = relationship("Answer", back_populates="answered_by")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    tag_word = Column(String, unique=True, index=True)

    questions = relationship("QuestionTag", back_populates="tag")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    ques_content = Column(String)
    views = Column(Integer, default=1)
    answered = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    votes = Column(Integer, default=0)
    has_accepted_answer = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="questions")

    tags = relationship("QuestionTag", back_populates="question")
    answers = relationship("Answer", back_populates="question")
    Votes = relationship("UserVote", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    ans_content = Column(String)
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    answered_by = relationship("User", back_populates="answers")

    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")

class QuestionTag(Base):
    __tablename__ = "question_tags"

    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    question = relationship("Question", back_populates="tags")
    tag = relationship("Tag", back_populates="questions")
