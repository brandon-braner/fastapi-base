from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()


@router.get("/", name="home")
async def root(request: Request):
    return {"message": "index"}
