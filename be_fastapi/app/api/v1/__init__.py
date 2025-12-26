from fastapi import APIRouter
from app.api.v1 import auth_api

# 1. Create one Master Router
api_router = APIRouter()

# 2. Register all feature routers here
api_router.include_router(auth_api.router)