from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from app.config.settings import settings
from app.modules.auth.providers.auth0 import oauth

router = APIRouter()


@router.get("/login", name="login")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    return await oauth.auth0.authorize_redirect(request, redirect_uri)


# @router.get("/login_callback", name="login_callback")
# @router.post("/login_callback", name="login_callback")
# async def callback(request: Request):
#     token = await oauth.auth0.authorize_access_token(request)
#     user = token['userinfo']
#     request.session['user'] = user
#     return dict(user)


@router.get("/callback", response_class=RedirectResponse)
@router.post("/callback", response_class=RedirectResponse)
async def callback(request: Request, response: RedirectResponse):
    token = await oauth.auth0.authorize_access_token(request)
    response_url = request.url_for("dashboard")
    response = RedirectResponse(response_url)
    response.set_cookie(settings.auth.id_token_cookie_name, token["id_token"], max_age=token["expires_at"], httponly=True)
    return response


@router.get("/logout", response_class=RedirectResponse)
def logout(request: Request):
    request.session.clear()
    request.cookies.clear()
    return f"""https://{settings.auth0_domain}/v2/logout?client_id={settings.auth0_client_id}&returnTo={request.url_for('home')}"""
