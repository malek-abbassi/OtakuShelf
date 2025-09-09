from typing import Union

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import emailpassword, session

init(
    app_info=InputAppInfo(
        app_name="OtakuShelf",
        api_domain="http://127.0.0.1:8000",
        website_domain="http://127.0.0.1:3000",
        api_base_path="/auth",
        website_base_path="/auth",
    ),
    supertokens_config=SupertokensConfig(
        connection_uri="http://localhost:3567",
        api_key="someApiKey123123123123" # should match with supertokens setup in docker-compose.yml
    ),
    framework="fastapi",
    recipe_list=[
        session.init(),  # initializes session features
        emailpassword.init(),
    ],
    mode="asgi",  # use wsgi if you are running using gunicorn
)

app = FastAPI(title="OtakuShelf")

# Add SuperTokens middleware
app.add_middleware(get_middleware())


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)
