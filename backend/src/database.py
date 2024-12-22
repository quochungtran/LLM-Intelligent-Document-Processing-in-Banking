import os

from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "root_password")
MYSQL_HOST = os.getenv("MYSQL_HOST", "0.0.0.0")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3308")

# MySQL database configuration
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/demo_bot"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # Improve connection resilience
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()