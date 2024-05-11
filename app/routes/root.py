from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

# @router.get("/")
# def read_root():
#     return JSONResponse(content={"Hello": "World"}, status_code=200)

@router.get("/health")
def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)