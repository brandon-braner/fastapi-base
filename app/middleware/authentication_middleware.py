from fastapi import Request
from starlette.authentication import AuthenticationBackend, AuthenticationError

from app.config.settings import settings
from app.modules.auth.providers.auth0 import validate_token


def add_protected_route(route: str):
    settings.protected_routes.append(route)


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        needs_authorization = await self.request_needs_authorization(request)
        if not needs_authorization:
            return

        authorization_cookie = await self.get_authorization_cookie(request)

        # return a 401 if they are not authenticated
        if not authorization_cookie:
            raise AuthenticationError("Unable to authenticate user.")

        validate_token(authorization_cookie)

    async def request_needs_authorization(self, request: Request):
        """
        If Path is in NON AUTH ENDPOINTS this will return false so we don't need to authenticate user the endpoint.
        """
        path = request.url.path
        path_split = path.split("/")  # get the prefix we assign to routes for app paths such as /dashboard
        route_prefix = f"/{path_split[1]}"
        return route_prefix in settings.protected_routes

    async def get_request_host(self, request: Request):
        return request.headers.get("Host", None)

    async def get_authorization_cookie(self, request: Request):
        """Get the cookie and return it that should be the auth token."""
        cookie_name = settings.id_token_cookie_name
        return request.cookies.get(cookie_name, None)
