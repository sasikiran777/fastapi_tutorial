from pydantic import BaseModel


class Books(BaseModel):
    name: str
    description: str
    user_id: int


class BookCreate(Books):
    pass

