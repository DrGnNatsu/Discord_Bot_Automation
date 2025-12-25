import uvicorn
from fastapi import FastAPI
from app.api.v1 import api_router
from app.core.config import settings
from app.exception.base_exception import AppException
from app.exception.handler import app_exception_handler

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Exception handler
app.add_exception_handler(AppException, app_exception_handler)

# Include all routers from api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)