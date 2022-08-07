from os import environ as env

from pydantic import BaseSettings


class Oauth2ProviderSettings(BaseSettings):
    client_id: str
    client_secret: str
    domain: str
    scope: str
    algorithm: str = "RS256"
    audience: str
    issuer: str


class Auth0Settings(Oauth2ProviderSettings):
    # Auth0 Settings
    client_id: str = env.get("AUTH0_CLIENT_ID", "Auth0 Client Id Needs to be set")
    client_secret: str = env.get("AUTH0_CLIENT_SECRET", "Auth0 Client Secret Needs to be set")
    domain: str = env.get("AUTH0_DOMAIN", "Auth0 Domain Needs to be set")
    scope: str = "openid profile email offline_access"
    algorithm: str = "RS256"
    audience: str = env.get("AUTH0_AUDIENCE", "Auth0 Audience Needs to be set")
    issuer: str = env.get("AUTH0_ISSUER", "Auth0 Issuer Needs to be set")


class AuthSettings(BaseSettings):
    # Auth Settings
    protected_routes: list = []
    session_cookie_name: str = "session"
    id_token_cookie_name: str = "id_token"

    provider_settings: Oauth2ProviderSettings = Auth0Settings()
