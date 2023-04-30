from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields


class Books(Model):
    # Primary key field is created automatically
    # id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    user = fields.ForeignKeyField('models.User', related_name="author")

    def __str__(self):
        return self.name


class User(Model):
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100)
    password = fields.CharField(max_length=50)
    phone = fields.CharField(max_length=20)

    def __str__(self):
        return self.name


books_pydantic = pydantic_model_creator(Books, name="Books")
books_pydantic_in = pydantic_model_creator(Books, name="BooksIn", exclude_readonly=True)

user_pydantic = pydantic_model_creator(User, name="User")
user_pydantic_in = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

