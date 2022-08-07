from fastapi import APIRouter
from fastapi_jinja import template
from starlette.requests import Request

router = APIRouter()


@router.get("/", name="home")
@template("marketing_pages/index.html")
async def root(request: Request):
    return {}
