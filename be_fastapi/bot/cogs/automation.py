import json
import logging

import discord
from discord.ext import commands

from app.db.session import SessionLocal
from app.models import Workflow
from bot.utils.logic_evaluator import evaluate_condition
from bot.utils.recursive_dispatcher import execute_instructions

logger = logging.getLogger(__name__)


class AutomationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Prevent infinite loops (Bot talking to itself)
        if message.author.bot:
            return

        # 1. Open Database Session
        session = SessionLocal()
        try:
            # 2. Query for Active Workflows
            workflows = session.query(Workflow).filter(
                Workflow.trigger_event == "message"
            ).all()

            if not workflows:
                return

            # 3. Process Workflows
            for flow in workflows:
                data = flow.compiled_json

                # Convert string to JSON if needed
                if isinstance(data, str):
                    data = json.loads(data)

                # Check if there is a top-level filter (Optional optimization)
                if data.get("filter"):
                    if not evaluate_condition(data["filter"], message):
                        continue

                # 4. EXECUTE THE BRAIN
                print(f"🚀 Triggering Workflow: {flow.id} and name {flow.name}")
                actions = data.get("actions", [])

                # Pass the instructions to the Dispatcher
                await execute_instructions(actions, message)

        except Exception as e:
            print(f"🔥 Runtime Error: {e}")
        finally:
            session.close()


async def setup(bot):
    await bot.add_cog(AutomationCog(bot))
