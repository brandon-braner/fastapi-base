from fastapi import APIRouter
from starlette.requests import Request
from singlepane.modules.auth.providers.auth0 import oauth
from singlepane import settings
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/login", name="login")
async def login(request: Request):
    redirect_uri = request.url_for('callback')
    return await oauth.auth0.authorize_redirect(request, redirect_uri)


# @router.get("/login_callback", name="login_callback")
# @router.post("/login_callback", name="login_callback")
# async def callback(request: Request):
#     token = await oauth.auth0.authorize_access_token(request)
#     user = token['userinfo']
#     request.session['user'] = user
#     return dict(user)

@router.get("/callback")
@router.post("/callback")
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    user = token['userinfo']
    request.session['user'] = user
    return dict(user)

@router.get("/logout", response_class=RedirectResponse)
def logout(request: Request):
    request.session.clear()
    return f"""https://{settings.auth0_domain}
        /v2/logout?client_id={settings.auth0_client_id}&returnTo={request.url_for('home')}"""
