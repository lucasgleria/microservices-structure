# calculator-service/cache.py

import aioredis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

async def get_redis():
    return await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def get_cache(key: str):
    redis = await get_redis()
    value = await redis.get(key)
    await redis.close()
    return value

async def set_cache(key: str, value: str, expire: int = 60):
    redis = await get_redis()
    await redis.set(key, value, ex=expire)
    await redis.close()
