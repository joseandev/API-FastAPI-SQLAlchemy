from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="My first API with Python",
    description="Lorem Ipsum Dolo Sit Amet",
    version="0.0.4",
    openapi_tags=[{
        "name": "users",
        "description": "users routes"
    }]
)

app.include_router(user)