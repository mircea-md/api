from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import mongo_url


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect():
    db.client = AsyncIOMotorClient(mongo_url)
    print(f'Connected to mongo at {mongo_url}')


async def close():
    db.client.close()
    print('Closed connection with mongo')
