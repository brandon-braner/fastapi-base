from auth0.v3.authentication.token_verifier import (
    AsymmetricSignatureVerifier,
    TokenVerifier,
)
from authlib.integrations.starlette_client import OAuth

from app.config.settings import settings

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.auth0_client_id,
    client_secret=settings.auth0_client_secret,
    client_kwargs={
        "scope": f"{settings.auth0_scope}",
    },
    server_metadata_url=f"https://{settings.auth0_domain}/.well-known/openid-configuration",
)


def validate_token(token: str) -> None:
    """
    Validate the token against the Auth0 server.
    Will raise an TokenValidationError if the token is invalid.
    """
    domain = settings.auth0_domain
    client_id = settings.auth0_client_id
    jwks_url = f"https://{domain}/.well-known/jwks.json"
    issuer = f"https://{domain}/"

    sv = AsymmetricSignatureVerifier(jwks_url)
    tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=client_id)

    tv.verify(token)
