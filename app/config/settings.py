from os import environ as env

from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file if exists
load_dotenv()

app_base_url = env.get("APP_URL", "http://localhost:8000")


class Settings(BaseSettings):
    app_name: str = "Single Pane"
    app_secret_key: str = env.get("APP_SECRET_KEY", "super-secret")
    app_url: str = f"{app_base_url}/app"
    # Auth Settings
    protected_routes: list = []
    auth_cookie_name: str = "session"

    # Auth0 Settings
    auth0_client_id: str = env.get("AUTH0_CLIENT_ID", "Auth0 Client Id Needs to be set")
    auth0_client_secret: str = env.get("AUTH0_CLIENT_SECRET", "Auth0 Client Secret Needs to be set")
    auth0_domain: str = env.get("AUTH0_DOMAIN", "Auth0 Domain Needs to be set")
    auth0_scope: str = "openid profile email offline_access"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
