from fastapi import APIRouter

from app.routes import idempotent, redis, root

path_prefix = "/v1"

router = APIRouter()
router.include_router(idempotent.router, tags=["idempotent payment api"], prefix=path_prefix)
router.include_router(root.router, tags=["root"], prefix=path_prefix)
router.include_router(redis.router, tags=["fetch from redis"], prefix=path_prefix)