import os
from os import environ as env
from pathlib import Path

import fastapi_jinja
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file if exists
load_dotenv()

app_base_url = env.get("APP_URL", "http://localhost:8000")


class Settings(BaseSettings):
    app_name: str = "Single Pane"
    app_secret_key: str = env.get("APP_SECRET_KEY", "super-secret")
    app_url: str = f"{app_base_url}/app"
    dev_mode: bool = env.get("DEV_MODE", False)
    # Auth Settings
    protected_routes: list = []
    session_cookie_name: str = "session"
    id_token_cookie_name: str = "id_token"

    # Auth0 Settings
    auth0_client_id: str = env.get("AUTH0_CLIENT_ID", "Auth0 Client Id Needs to be set")
    auth0_client_secret: str = env.get("AUTH0_CLIENT_SECRET", "Auth0 Client Secret Needs to be set")
    auth0_domain: str = env.get("AUTH0_DOMAIN", "Auth0 Domain Needs to be set")
    auth0_scope: str = "openid profile email offline_access"
    auth0_algorithm: str = "RS256"
    auth0_audience: str = env.get("AUTH0_AUDIENCE", "Auth0 Audience Needs to be set")
    auth0_issuer: str = env.get("AUTH0_ISSUER", "Auth0 Issuer Needs to be set")


def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# setup jinja
path = Path(__file__).resolve().parent
folder = path.parent.resolve()
template_folder = os.path.join(folder, "templates")
template_folder = os.path.abspath(template_folder)

fastapi_jinja.global_init(template_folder, auto_reload=settings.dev_mode)
