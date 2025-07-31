from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = (os.getenv("DATABASE_PUBLIC_URL") or os.getenv("DATABASE_URL") or "").strip()

if not SQLALCHEMY_DATABASE_URL:

    db_username = os.getenv("POSTGRES_USER") or os.getenv("PGUSER")
    db_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("PGPASSWORD")
    db_host = os.getenv("POSTGRES_HOST") or os.getenv("PGHOST")
    db_name = os.getenv("POSTGRES_DB") or os.getenv("PGDATABASE")

    if not all([db_username, db_password, db_host, db_name]):
        raise Exception("Database credentials are missing in environment variables")

    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
    )

if "railway" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+psycopg://"),
        connect_args={
            "sslmode": "require"
        }
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+psycopg://"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
