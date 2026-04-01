from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os 

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/fintech")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autoflush=False, autocommit = False, bind=engine)

Base = declarative_base()