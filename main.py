    # main.py
from fastapi import FastAPI
from database import engine
import models
from routers import freelancers

app = FastAPI(title="Freelancer API")
models.Base.metadata.create_all(bind=engine)

app.include_router(freelancers.router)
