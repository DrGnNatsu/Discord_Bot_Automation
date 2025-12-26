import logging
import uvicorn
from fastapi import FastAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

from app.api.v1 import api_router
from app.core.config import settings
from app.core.cors import setup_cors
from app.exception.base_exception import AppException
from app.exception.handler import app_exception_handler

app = FastAPI()

setup_cors(app)

# Exception handler
app.add_exception_handler(AppException, app_exception_handler)

# Include all routers from api_router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
