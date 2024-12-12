from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from mangum import Mangum
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
from sqlalchemy.sql import func

load_dotenv()

db_username = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_name = os.getenv("POSTGRES_DB")

if not all([db_username, db_password, db_host, db_name]):
    raise HTTPException(
        status_code=500,
        detail="Database credentials not found in the environment variables",
    )

if not all([db_username, db_password, db_host, db_name]):
    raise HTTPException(
        status_code=500, detail="Database credentials not found in the secret"
    )

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
)
if not SQLALCHEMY_DATABASE_URL:
    raise HTTPException(status_code=500, detail="DB_URL not found in the secret")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quote = Column(String, nullable=False, unique=True)
    season = Column(Integer, nullable=False)
    episode = Column(Integer, nullable=False)
    character = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)

app = FastAPI()
handler = Mangum(app)


class QuoteSchema(BaseModel):
    quote: str
    season: int
    episode: int
    character: str

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return RedirectResponse(url="/getquotes/")


@app.get("/getquotes/", response_model=List[QuoteSchema])
def read_quotes(db: Session = Depends(get_db)):
    quotes = db.query(Quote).all()
    return quotes


@app.get("/frank/random/", response_model=QuoteSchema)
def get_random_quote(db: Session = Depends(get_db)):
    quote = (
        db.query(Quote)
        .filter(Quote.character == "Frank Costanza")
        .order_by(func.random())
        .first()
    )
    if not quote:
        raise HTTPException(status_code=404, detail="No quotes found")
    return quote


@app.get("/george/random/", response_model=QuoteSchema)
def get_random_quote(db: Session = Depends(get_db)):
    quote = (
        db.query(Quote)
        .filter(Quote.character == "George Costanza")
        .order_by(func.random())
        .first()
    )
    if not quote:
        raise HTTPException(status_code=404, detail="No quotes found")
    return quote


@app.get("/quote/random/", response_model=QuoteSchema)
def get_random_quote(db: Session = Depends(get_db)):
    quote = db.query(Quote).order_by(func.random()).first()
    if not quote:
        raise HTTPException(status_code=404, detail="No quotes found")
    return quote


@app.get("/quotes/{character}/", response_model=List[QuoteSchema])
def get_quotes_by_character(character: str, db: Session = Depends(get_db)):
    quotes = db.query(Quote).filter(Quote.character.ilike(f"%{character}%")).all()
    if not quotes:
        raise HTTPException(
            status_code=404, detail="No quotes found for this character"
        )
    return quotes


@app.post("/createquotes/", response_model=QuoteSchema)
def create_quote(quote: QuoteSchema, db: Session = Depends(get_db)):
    existing_quote = db.query(Quote).filter(Quote.quote == quote.quote).first()
    if existing_quote:
        raise HTTPException(status_code=400, detail="Quote already exists")
    db_quote = Quote(**quote.dict())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote


@app.post("/createquotes/bulk/", response_model=List[QuoteSchema])
def create_quotes_bulk(quotes: List[QuoteSchema], db: Session = Depends(get_db)):
    db_quotes = []
    for quote in quotes:
        existing_quote = db.query(Quote).filter(Quote.quote == quote.quote).first()
        if existing_quote:
            raise HTTPException(
                status_code=400, detail=f"Quote '{quote.quote}' already exists"
            )
        db_quote = Quote(**quote.dict())
        db.add(db_quote)
        db_quotes.append(db_quote)
    db.commit()
    for db_quote in db_quotes:
        db.refresh(db_quote)
    return db_quotes
