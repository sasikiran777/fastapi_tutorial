from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body

from constants import books

app = FastAPI(
    title="Fast API Advance",
    description="Fast API basic tutorial🚀",
    version="1.0.0",
)


@app.get("/")
async def home():
    return {'message': 'This is home'}


@app.get('/books')
async def list_books():
    return books


@app.get('/books/{id}')
async def get_book(book_id: int, book_name: Optional[str] = None):
    result = []
    for i in books:
        if i['id'] is book_id:
            if book_name:
                if i['author'].casefold() == book_name.casefold():
                    result.append(i)
            else:
                result.append(i)
    return result


@app.post('/books/create')
async def create_book(book=Body()):
    books.append(book)
    return books


@app.put('/books/update')
async def update_book(book=Body()):
    for i, value in enumerate(books):
        if value['id'] == int(book.get('id')):
            books[i] = book
            break
    return books


@app.delete('/books/{id}')
async def delete_book(book_id: int):
    for i in range(len(books)):
        if books[i]['id'] == book_id:
            books.pop(i)
    return books
