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


