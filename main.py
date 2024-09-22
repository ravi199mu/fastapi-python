from fastapi import FastAPI,HTTPException
import random
import os
import json
from pydantic import BaseModel
from typing import Literal,Optional
from uuid import uuid4
from fastapi.encoders import jsonable_encoder


app = FastAPI()


class Book(BaseModel):
    name: str
    price:float
    genre : Literal["fiction",'non-fiction']
    book_id: Optional[str] = uuid4().hex


BOOKS_FILE = "books.json"
BOOKS_DATABASE = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, 'r') as f:
        BOOKS_DATABASE = json.load(f)

@app.get("/")
async def home():
    return {"message":"Welcome to my bookstore"}


@app.get("/list-books")
async def list_books():
    return {"books":BOOKS_DATABASE}


@app.get("/book-by-index/{index}")
async def book_by_index(index:int):
    if index < 0 or index >= len(BOOKS_DATABASE):
        raise HTTPException(404,f"invalid index, Book not found")
    else:
        return {"book":BOOKS_DATABASE[index]}
    

@app.get("/get-random-book")
async def get_random_book():
    return {"book":random.choice(BOOKS_DATABASE)}


@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOKS_DATABASE.append(json_book)
    with open(BOOKS_FILE, 'w') as f:
        json.dump(BOOKS_DATABASE,f)
    return {"message" : "Book added to store."}
    

# query param
# ?book_id=dadfafaf
@app.get("/get_book")
async def get_book(book_id:str):
    for book in BOOKS_DATABASE:
        if book["book_id"] == book_id:
            return book
        
    raise HTTPException(404,f"book not found for {book_id}")