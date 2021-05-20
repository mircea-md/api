import hashlib
import time
from datetime import datetime

import bson
import pymongo
import pytz
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import ReturnDocument

from config.settings import mongo_db
from models.default import SuccessResponse
from models.user import UserIn, UserInDB, UserOut, UserBase


def generate_hash(message: str) -> str:
    hash_to_digest = hashlib.sha1(message.encode('utf-8'))
    return hash_to_digest.hexdigest()


def epoch_time() -> int:
    return int(time.mktime(
        datetime.now(tz=pytz.timezone('Europe/Chisinau')).timetuple()))


async def create_user(api_user: UserIn,
                      cli: AsyncIOMotorClient) -> BaseModel:
    hashed_password = generate_hash(api_user.password)
    api_user = UserInDB(**api_user.dict(),
                        created_at=epoch_time(),
                        last_login=0,
                        hashed_password=hashed_password)

    row = await cli[mongo_db]['users'].insert_one(api_user.dict())

    return UserOut(**api_user.dict(), id=str(row.inserted_id))


async def update_user(_id: str,
                      api_user: UserBase,
                      cli: AsyncIOMotorClient) -> BaseModel:
    if not bson.ObjectId.is_valid(_id):
        return UserOut()

    row = await cli[mongo_db]['users'].find_one_and_update({'_id': bson.ObjectId(_id)},
                                                           {'$set': api_user.dict()},
                                                           return_document=ReturnDocument.AFTER)
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")

    row['id'] = str(row['_id'])

    return UserOut(**row)


async def get_user(_id: str,
                   cli: AsyncIOMotorClient) -> BaseModel:
    if not bson.ObjectId.is_valid(_id):
        return UserOut()

    row = await cli[mongo_db]['users'].find_one({'_id': bson.ObjectId(_id)})
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")

    row['id'] = str(row['_id'])

    return UserOut(**row)


async def get_users(skip: int,
                    take: int,
                    cli: AsyncIOMotorClient) -> [BaseModel]:
    rows = await cli[mongo_db]['users'].find({}).sort('created_at',
                                                      pymongo.DESCENDING).skip(skip).limit(take).to_list(length=take)
    result = []
    for row in rows:
        row['id'] = str(row['_id'])
        result.append(UserOut(**row))

    return result


async def delete_user(_id: str,
                      cli: AsyncIOMotorClient) -> BaseModel:
    if not bson.ObjectId.is_valid(_id):
        return SuccessResponse(success=False)

    row = await cli[mongo_db]['users'].delete_one({'_id': bson.ObjectId(_id)})

    return SuccessResponse(success=row.deleted_count > 0)


async def get_admin_user(first_name: str,
                         last_name: str,
                         password: str,
                         cli: AsyncIOMotorClient) -> dict:
    row = await cli[mongo_db]['users'].find_one({'first_name': first_name,
                                                 'last_name': last_name,
                                                 'hashed_password': generate_hash(password),
                                                 'is_active': True,
                                                 'role': 'admin'})

    return row
