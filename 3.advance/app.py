from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

from errors.not_found import NotFoundError
from routes import user, books

app = FastAPI(
    title="Fast API Advance",
    description="Fast API Advance tutorial🚀",
    version="1.0.0",
)

app.include_router(user.router)
app.include_router(books.router)


@app.exception_handler(NotFoundError)
async def not_found_error(request: Request, exception: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=
        {
            "message": f"{exception.message}",
            "Status": "Failed"
        })


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
