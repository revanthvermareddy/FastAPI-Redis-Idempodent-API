from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger
from app.services.redis.service import redis_connector

router = APIRouter()

@router.get("/fetch")
def fetch_value(key: str  = "MCH-945b0379-cf9c-4476-8677-8bf78474d85e"):
    """
    Fetch a value from Redis
    """
    try:
        value = redis_connector.get_value(key)
        return JSONResponse(content={"key": key, "value": value}, status_code=200)
    except Exception as ex:
       logger.error(f"Error fetching value from Redis: {ex}")
       return JSONResponse(content={"error": "Error fetching value from Redis"}, status_code=500)