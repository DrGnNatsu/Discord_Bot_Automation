import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.v1 import api_router
from app.core.config import settings
from app.core.cors import setup_cors
from app.exception.base_exception import AppException
from app.exception.handler import app_exception_handler
from bot.client import get_discord_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --- Bot Setup ---
bot = get_discord_client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run the discord bot
    logger.info("Starting Discord bot...")
    task = asyncio.create_task(bot.start(settings.DISCORD_TOKEN))
    yield
    # Shutdown: Close the bot
    logger.info("Shutting down Discord bot...")
    await bot.close()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Discord bot task cancelled.")


app = FastAPI(lifespan=lifespan)

setup_cors(app)

# Exception handler
app.add_exception_handler(AppException, app_exception_handler)

# Include all routers from api_router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"status": "System Online", "bot_user": str(bot.user)}


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
