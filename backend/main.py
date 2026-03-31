from fastapi import FastAPI
import models
from db import engine
from fastapi.middleware.cors import CORSMiddleware
from routes import router

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def greet():
    return "Welcome to Backend of this Fintech project"



