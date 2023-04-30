from fastapi import APIRouter, status
from tortoise.exceptions import DoesNotExist

from errors.not_found import NotFoundError
from models.models import books_pydantic, Books, books_pydantic_in, User, user_pydantic
from schema.book import BookCreate

router = APIRouter(tags=["Books"], prefix='/books', responses={200: {"description": "Success"}})


@router.post('/', name="Create Books", description="To create a book")
async def create_book(data: BookCreate):
    try:
        user = await user_pydantic.from_queryset_single(User.get(id=data.user_id))
        book = data.dict(exclude_unset=True)
        book = await Books.create(**book, author=user)
        response = await books_pydantic_in.from_tortoise_orm(book)
        return {
            "status": "Success",
            "data": response
        }
    except DoesNotExist:
        raise NotFoundError(f"User not found with id: {data.user_id}")


@router.get('/', name="Get Books", description="All books")
async def get_books():
    books = await books_pydantic.from_queryset(Books.all())
    return {
        "status": "Success",
        "data": books
    }


@router.get('/{book_id}', name="Get A Book", description="Get a specific book")
async def get_book(book_id: int):
    book = await books_pydantic.from_queryset_single(Books.get(id=book_id))
    return {
        "status": "Success",
        "data": book
    }


@router.get('/user/{user_id}', name="User Books", description="All books writen by a user")
async def get_user_books(user_id: int):
    books = await books_pydantic.from_queryset(Books.filter(user_id=user_id))
    return {
        'status_code': 200,
        "status": "Success",
        "data": books,
    }


@router.put('/{book_id}', name="Update A Books", description="To update a book")
async def update_book(book_id: int, data: BookCreate):
    try:
        user = await user_pydantic.from_queryset_single(User.get(id=data.user_id))
        book = await Books.get(id=book_id)
        book.name = data.name
        book.description = data.description
        book.user_id = user.id
        await book.save()
        response = await books_pydantic.from_tortoise_orm(book)
        return {
            "status": "Success",
            "data": response
        }
    except DoesNotExist:
        raise NotFoundError(f"User not found with id: {data.user_id}")


@router.delete('/{book_id}', name="Get Books", description="All books")
async def delete_book(book_id: int):
    await Books.filter(id=book_id).delete()
    return {
        "status": "Success",
        "data": "Book deleted"
    }
