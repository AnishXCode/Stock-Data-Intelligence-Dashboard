from fastapi import FastAPI
import models
from db import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def greet():
    return "Welcome to Backend of this Fintech project"

@app.get("/companies")
def get_all_companies():
    return "These are all the available companies"





