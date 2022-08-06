from functools import lru_cache

from pydantic import BaseSettings
from os import environ as env


class Settings(BaseSettings):
    app_name: str = "Single Pane"
    app_secret_key: str = env.get("APP_SECRET_KEY", "super-secret")
    auth0_client_id: str = env.get("AUTH0_CLIENT_ID", "Auth0 Client Id Needs to be set")
    auth0_client_secret: str = env.get("AUTH0_CLIENT_SECRET", "Auth0 Client Secret Needs to be set")
    auth0_domain: str = env.get("AUTH0_DOMAIN", "Auth0 Domain Needs to be set")
    auth0_scope: str = "openid profile email offline_access"


def get_settings() -> Settings:
    return Settings()
