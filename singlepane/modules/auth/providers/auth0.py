from authlib.integrations.starlette_client import OAuth
from singlepane.settings import get_settings

settings = get_settings()
oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.auth0_client_id,
    client_secret=settings.auth0_client_secret,
    client_kwargs={
        "scope": f"{settings.auth0_scope}",
    },
    server_metadata_url=f'https://{settings.auth0_domain}/.well-known/openid-configuration',
)