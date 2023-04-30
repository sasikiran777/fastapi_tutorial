from fastapi.security import OAuth2PasswordRequestForm
import bcrypt

from custom_errors.unauth_error import UnauthorizedException


def hash_user_password(password: str):
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())


def verify_password(password, hashed_password) -> bool:
    return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(hashed_password, 'utf-8'))


async def generate_token_service(form_data: OAuth2PasswordRequestForm):
    if form_data.username == 'sasi@gmail.com' and form_data.password == 'Asd@1234':
        return {
            'id': 1,
            'name': 'sasi kiran',
            'email': 'sasi@gmail.com',
            'phone': '8500035146'
        }
    raise RuntimeError("In valid user")
    # raise UnauthorizedException("User Not Found")

