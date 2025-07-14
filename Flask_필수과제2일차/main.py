from fastapi import FastAPI, HTTPException
from schemas import Book
from models import BookModel

app = FastAPI()
book_db = BookModel()

@app.get("/books")
def get_books():
    return book_db.get_all()

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = book_db.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books")
def create_book(book: Book):
    return book_db.create(book.dict())

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    updated_book = book_db.update(book_id, book.dict())
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    deleted = book_db.delete(book_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message" : "Book deleted successfully"}  