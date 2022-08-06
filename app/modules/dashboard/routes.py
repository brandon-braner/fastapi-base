from fastapi import APIRouter
from starlette.requests import Request

from app.middleware.authentication_middleware import add_protected_route

router = APIRouter(prefix="/dashboard")
add_protected_route("/dashboard")


@router.get("/", name="dashboard")
async def root(request: Request):
    return {"message": "dashboard"}
