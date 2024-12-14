from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from pydantic import BaseModel

from app.db import get_db
from app.models import Quote

router = APIRouter()


class QuoteSchema(BaseModel):
    quote: str
    season: int
    episode: int
    character: str

    class Config:
        orm_mode = True


@router.get("/getquotes/", response_model=List[QuoteSchema])
def read_quotes(db: Session = Depends(get_db)):
    quotes = db.query(Quote).all()
    return quotes


@router.get("/frank/random/", response_model=QuoteSchema)
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


@router.get("/george/random/", response_model=QuoteSchema)
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


@router.get("/quote/random/", response_model=QuoteSchema)
def get_random_quote(db: Session = Depends(get_db)):
    quote = db.query(Quote).order_by(func.random()).first()
    if not quote:
        raise HTTPException(status_code=404, detail="No quotes found")
    return quote


@router.get("/quotes/{character}/", response_model=List[QuoteSchema])
def get_quotes_by_character(character: str, db: Session = Depends(get_db)):
    quotes = db.query(Quote).filter(Quote.character.ilike(f"%{character}%")).all()
    if not quotes:
        raise HTTPException(
            status_code=404, detail="No quotes found for this character"
        )
    return quotes


@router.post("/createquotes/", response_model=QuoteSchema)
def create_quote(quote: QuoteSchema, db: Session = Depends(get_db)):
    existing_quote = db.query(Quote).filter(Quote.quote == quote.quote).first()
    if existing_quote:
        raise HTTPException(status_code=400, detail="Quote already exists")
    db_quote = Quote(**quote.dict())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote


@router.post("/createquotes/bulk/", response_model=List[QuoteSchema])
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
