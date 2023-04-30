from fastapi import APIRouter
from models.models import user_pydantic_in, User, user_pydantic
from starlette.responses import JSONResponse

router = APIRouter(tags=["Users"], prefix='/users', responses={200: {"description": "Success"}})


@router.post('/', name="Create User", description="To create a user")
async def create_user(user: user_pydantic_in):
    try:
        new_user = await User.create(**user.dict(exclude_unset=True))
        response = await user_pydantic.from_tortoise_orm(new_user)
        return {
            'status_code': 200,
            "status": "Success",
            "data": response,
        }
    except Exception as er:
        return JSONResponse(
            status_code=400,
            content={
                "message": f"{er}",
                "status": "Failed"
            }
        )


@router.get('/', name="Get All Users", description="List all users in data base")
async def users():
    members = await user_pydantic.from_queryset(User.all())
    return {
        'status_code': 200,
        "status": "Success",
        "data": members,
    }


@router.get('/{user_id}', name="Get A Users", description="Get a specific user")
async def get_user(user_id: int):
    user = await user_pydantic.from_queryset_single(User.get(id=user_id))
    return {
        "status_code": 200,
        "status": "Success",
        "data": user
    }


@router.put('/{user_id}', name="Update A Users", description="Update a specific user")
async def update_user(user_id: int, modify_user: user_pydantic_in):
    user = await User.get(id=user_id)
    modify_user = modify_user.dict(exclude_unset=True)
    user.name = modify_user.get('name')
    user.email = modify_user.get('email')
    user.password = modify_user.get('password')
    user.phone = modify_user.get('phone')
    await user.save()
    response = await user_pydantic_in.from_tortoise_orm(user)
    return {
        "status_code": 200,
        "status": "Success",
        "data": response
    }


@router.delete('/{user_id}', name="Delete A Users", description="Delete a specific user with all related foreign keys")
async def delete_user(user_id: int):
    await User.filter(id=user_id).delete()
    return {
        "status_code": 200,
        "status": "Success",
        "data": "ok"
    }
