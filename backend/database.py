import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_URL = os.getenv("DB_URL", "").strip()

# Zero-config fallback: local SQLite file so the project runs immediately.
# Swap DB_URL in .env with a MySQL URI for production:
#   mysql+pymysql://user:password@localhost:3306/agripredic
if not DB_URL:
    DB_URL = "sqlite:///./agripredic.db"

connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

engine = create_engine(DB_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
