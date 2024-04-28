from fastapi import FastAPI
from App import models
from App.database import engine
from App.routers import user, authentication, question, answer
app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(question.router)
app.include_router(answer.router)
app.include_router(user.router)

# Sql Admin
from sqladmin import Admin, ModelView
from App.models import User, Question
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.email, User.ans_given]

class QuestionAdmin(ModelView, model = Question):
    column_list = [Question.id, Question.title, Question.ques_content, Question.votes, Question.views, Question.tags]
admin.add_view(UserAdmin)
admin.add_view(QuestionAdmin)
