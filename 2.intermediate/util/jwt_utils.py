import os
from datetime import datetime
from datetime import timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    payload = {
        'sub': str(user_id),
        'email': email
    }
    # expires = datetime.datetime.utcnow() + expires_delta
    expires = datetime.utcnow() + expires_delta
    payload.update({'exp': expires})
    return jwt.encode(payload, os.environ.get("JWT_SECRET"), algorithm=os.environ.get("JWT_ALGO"))


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=os.environ.get("JWT_ALGO"))
        user_id = payload.get("sub")
        email = payload.get("email")

        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found",
                                headers={"WWW-Authenticate": "Bearer"})

        return {
            'id': 1,
            'name': 'Sasi Kiran',
            'email': 'sasiking93@gmail.com',
            'phone': '8500035146',
        }
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"{e}")
