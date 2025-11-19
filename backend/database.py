# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/reviewsdb")

# SQLAlchemy 2.0 style engine
engine = create_engine(DATABASE_URL, future=True, echo=False)

# SessionLocal factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Base model class
Base = declarative_base()
