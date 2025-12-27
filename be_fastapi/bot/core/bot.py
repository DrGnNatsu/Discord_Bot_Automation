from discord.ext import commands
import discord
import logging

logger = logging.getLogger(__name__)

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="|", intents=intents)

    async def setup_hook(self):
        # Load extensions (Cogs)
        extensions = [
            "bot.cogs.general",
            "bot.cogs.automation"
        ]
        
        for ext in extensions:
            try:
                await self.load_extension(ext)
                logger.info(f"Loaded extension: {ext}")
            except Exception as e:
                logger.error(f"Failed to load extension {ext}: {e}")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Latency: {self.latency * 1000:.2f} ms")
