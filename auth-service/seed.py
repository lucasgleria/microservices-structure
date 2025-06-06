# auth-service/seed.py

import asyncio
from database import db
from models import User
from auth import hash_password

async def seed():
    user = User(
        username="admin1",
        email="admin1@example.com",
        hashed_password=hash_password("1234567")
    )
    await db['users'].insert_one(user.to_dict())
    print("Seed completed.")

if __name__ == "__main__":
    asyncio.run(seed())
