from fastapi import FastAPI
from db_connection import database_connection
from pydantic import BaseModel


app = FastAPI()
db = database_connection()


class Book(BaseModel):
        isbn: str
        title: str
        author: str
        publish_date: str
        publisher: int


@app.get("/")
def read_root():
    return {"message: Hello!"}


@app.get("/books")
def read_books():
    return db.select_books()


@app.get("/books/{isbn}")
def get_book(isbn: str):
    return db.select_book(isbn)


@app.post("/books")
def post_book(book: Book):
     return db.create_book(book)