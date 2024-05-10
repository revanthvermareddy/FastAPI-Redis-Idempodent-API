from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.services.redis.service import redis_connector


@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect to redis cluster
    redis_connector.connect()
    yield
    # disconnect from the redis cluster
    redis_connector.disconnect()