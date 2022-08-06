from os import environ as env

import uvicorn
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

app = FastAPI()
load_dotenv()
app.add_middleware(SessionMiddleware, secret_key=env.get("APP_SECRET_KEY"))

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email offline_access",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


@app.get("/", name="home")
async def root(request: Request):
    url = request.url_for("home")
    return {"message": url}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('callback')
    return await oauth.auth0.authorize_redirect(request, redirect_uri)


@app.get("/callback")
@app.post("/callback")
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    user = token['userinfo']
    request.session['user'] = user
    return dict(user)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    redirect_url = f"https://{env.get('AUTH0_DOMAIN')}" \
                   f"/v2/logout?client_id={env.get('AUTH0_CLIENT_ID')}&returnTo={request.url_for('home')}"
    return RedirectResponse(redirect_url)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
