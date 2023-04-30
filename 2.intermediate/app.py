import os
from datetime import timedelta
from starlette.middleware.cors import CORSMiddleware
from custom_errors.unauth_error import UnauthorizedException
from middlewares.time import TimeMiddleware
from schema.login import UserLogin
from util.hashing import hash_user_password, verify_password, generate_token_service
from util.jwt_utils import create_access_token, get_current_user
from fastapi import FastAPI, Depends, Request, status
from fastapi.params import Body
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

app = FastAPI(
    title="Fast API Advance",
    description="Fast API Intermediate tutorial🚀",
    version="1.0.0",
)


app.add_middleware(TimeMiddleware)
origins = [
    "http://localhost:3500",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["PUT", "POST", "GET", "DELETE"],
    allow_headers=["*"],
)


# Password hashing
@app.get('/user/hash-password/{password}')
async def hashed_password(password: str):
    return {
        "hashed_password1": hash_user_password(password),
        "access_token": create_access_token("sasi@gmail.com", 123, timedelta(minutes=20))
    }


@app.post('/user/password-check')
async def check_password(data=Body()):
    return {
        "password_check": verify_password(
            data.get('password', 'Asd@1234'),
            data.get('hashed_password', '$2b$12$RFfEoz1TLc0Ah4uxbfc9weVgwA5VktJmft3D2/3L93C4Wg1MuzeQa')
        )
    }


# Authorizing User
@app.post('/user/login')
async def login(data: UserLogin):
    try:
        if verify_password(
                data.password,
                os.environ.get("HASHED_PASSWORD")
        ):
            return JSONResponse(
                status_code=200,
                content={
                    "access_token": create_access_token("sasi@gmail.com", 123, timedelta(minutes=20))
                })

    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={
                "message": f"{e}"
            })


# Get User Details After Authorizing
@app.get('/user')
async def get_user(user=Depends(get_current_user)):
    return user


# Generate Token For Swagger docs
@app.post('/auth/token', description="Generates access token for swagger docs", name="Generate Access Token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await generate_token_service(form_data)
        return JSONResponse(
            status_code=200,
            content={
                "access_token": create_access_token(user.get('email'), user.get('id'), timedelta(minutes=20))
            })
    except RuntimeError as er:
        return JSONResponse(
            status_code=400,
            content={
                "message": f"{er}"
            })


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exception: UnauthorizedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=
        {
            "data": {
                "message": f"{exception.message}"
            },
            "type": "Failed",
            "Status": status.HTTP_401_UNAUTHORIZED
        })
