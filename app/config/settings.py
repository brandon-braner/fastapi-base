import os
from os import environ as env
from pathlib import Path

import fastapi_jinja
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file if exists
load_dotenv()

app_base_url = env.get("APP_URL", "http://localhost:8000")
from app.config.auth import AuthSettings


class Settings(BaseSettings):
    app_name: str = "Single Pane"
    app_secret_key: str = env.get("APP_SECRET_KEY", "super-secret")
    app_url: str = f"{app_base_url}/app"
    dev_mode: bool = env.get("DEV_MODE", False)
    auth: AuthSettings = AuthSettings()


def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# setup jinja
path = Path(__file__).resolve().parent
folder = path.parent.resolve()
template_folder = os.path.join(folder, "templates")
template_folder = os.path.abspath(template_folder)

fastapi_jinja.global_init(template_folder, auto_reload=settings.dev_mode)
