from typing import List

from fastapi import APIRouter, Depends, Path
from motor.motor_asyncio import AsyncIOMotorClient

from auth.dependencies import admin_basic_auth
from db.crud.user import create_user, update_user, get_user, delete_user, get_users
from db.mongodb import get_database
from models.default import SuccessResponse
from models.user import UserOut, UserIn, UserBase

user_router = APIRouter()


@user_router.post("/user/", response_model=UserOut)
async def user_create(user_in: UserIn, db: AsyncIOMotorClient = Depends(get_database), ):
    user = await create_user(user_in, db)
    return user


@user_router.put("/user/{user_id}", response_model=UserOut)
async def user_update(*,
                      user_id: str = Path(None, title='user id', min_length=24, max_length=24),
                      user_in: UserBase,
                      db: AsyncIOMotorClient = Depends(get_database),
                      is_admin: bool = Depends(admin_basic_auth)):
    user = await update_user(user_id, user_in, db)
    return user


@user_router.get("/user/{user_id}", response_model=UserOut)
async def user_get(user_id: str = Path(None, title='user id', min_length=24, max_length=24),
                   db: AsyncIOMotorClient = Depends(get_database), ):
    user = await get_user(user_id, db)
    return user


@user_router.delete("/user/{user_id}", response_model=SuccessResponse)
async def user_delete(user_id: str = Path(None, title='user id', min_length=24, max_length=24),
                      db: AsyncIOMotorClient = Depends(get_database),
                      is_admin: bool = Depends(admin_basic_auth)):
    success = await delete_user(user_id, db)
    return success


@user_router.get("/users/", response_model=List[UserOut])
async def user_list(skip: int = 0, limit: int = 10, db: AsyncIOMotorClient = Depends(get_database), ):
    users = await get_users(skip, limit, db)
    return users
