import os

os.environ["db_host"] = "localhost"
os.environ["db_port"] = "5432"
os.environ["db_user"] = "postgres"
os.environ["db_pass"] = "postgres"
os.environ["db_name"] = "test_db"
os.environ["secret_key"] = "test_secret_key"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from datetime import datetime


@pytest.fixture
def get_test_user():
    return {
        "username": f"User{datetime.now().strftime('%H%M%S')}",
        "email": f"User{datetime.now().strftime('%H%M%S')}@example.com",
        "password": "1234566436",
    }

@pytest.fixture
def get_test_db():
    engine = create_engine(f"postgresql://postgres:postgres@localhost:5432/test_db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()