from fastapi import APIRouter
from app.api.v1 import auth_api
from app.api.v1 import deploy_api

# 1. Create one Master Router
api_router = APIRouter()

# 2. Register all feature routers here
api_router.include_router(auth_api.router)
api_router.include_router(deploy.router, tags=["Deploy"])