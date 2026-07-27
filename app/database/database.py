from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
)

# PostgreSQL Connection String එක සෑදීම
DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# Database Engine එක සාදාගැනීම
engine = create_engine(DATABASE_URL)

# Database Session එක සාදාගැනීම
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
# Connection Test එක සඳහා
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("✅ Database Connection Successful!")
    except Exception as e:
        print("❌ Connection Failed:", e)

from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()