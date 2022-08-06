from os import environ as env

from pydantic import BaseSettings


class Auth0Settings(BaseSettings):
    client_id: str = env.get("AUTH0_CLIENT_ID", "Auth0 Client Id Needs to be set")
    client_secret: str = env.get("AUTH0_CLIENT_SECRET", "Auth0 Client Secret Needs to be set")
    domain: str = env.get("AUTH0_DOMAIN", "Auth0 Domain Needs to be set")
    scope: str = "openid profile email offline_access"


class AuthSettings(BaseSettings):
    auth0: Auth0Settings = Auth0Settings()
