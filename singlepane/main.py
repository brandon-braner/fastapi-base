from os import environ as env

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from singlepane.settings import get_settings
app = FastAPI()


def bootstrap():
    """Bootstrap the application."""
    load_dotenv()
    settings = get_settings()
    configure_middleware()
    configure_routes()


def configure_middleware():
    app.add_middleware(SessionMiddleware, secret_key=env.get("APP_SECRET_KEY"))


def configure_routes():
    from singlepane.modules.auth.routes import router as auth_router
    from singlepane.modules.pages.routes import router as pages_router

    app.include_router(pages_router)
    app.include_router(auth_router)


bootstrap()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
