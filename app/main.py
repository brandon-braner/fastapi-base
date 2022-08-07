from os import environ as env

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.middleware.authentication_middleware import AuthBackend

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def bootstrap():
    """Bootstrap the application."""
    configure_middleware()
    configure_routes()


def configure_middleware():
    app.add_middleware(SessionMiddleware, secret_key=env.get("APP_SECRET_KEY"))
    app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())


def configure_routes():
    from app.modules.auth.routes import router as auth_router
    from app.modules.dashboard.routes import router as dashboard_router
    from app.modules.marketing_pages.routes import router as marketing_pages_router

    app.include_router(marketing_pages_router)
    app.include_router(dashboard_router)
    app.include_router(auth_router)


bootstrap()

if __name__ == "__main__":  # nosec
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec
