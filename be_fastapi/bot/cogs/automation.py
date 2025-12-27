import json
import logging

import discord
from discord.ext import commands

from app.db.session import SessionLocal
from app.models import Workflow
from bot.core.session_manager import get_user_session
from bot.utils.logic_evaluator import evaluate_condition
from bot.utils.recursive_dispatcher import execute_instructions

logger = logging.getLogger(__name__)


class AutomationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return

        # --- 1. CHECK FOR ACTIVE SESSION (Priority High) ---
        user_session = get_user_session(message.author.id)

        if user_session:
            # FIX: We use the 'workflow_id' (UUID) to find the logic, NOT the 'current_state' string.
            target_uuid = user_session.workflow_id

            print(f"🔄 User {message.author.name} is in session. Loading Workflow UUID: {target_uuid}")

            session_db = SessionLocal()
            try:
                # CORRECTION: Query by 'id' (UUID), not 'name' or 'state'
                state_flow = session_db.query(Workflow).filter(
                    Workflow.id == target_uuid
                ).first()

                if state_flow:
                    data = state_flow.compiled_json
                    if isinstance(data, str): data = json.loads(data)

                    print(f"🚀 Resuming Workflow: {state_flow.name}")
                    actions = data.get("actions", [])
                    await execute_instructions(actions, message)
                else:
                    print(f"⚠️ Critical Error: Workflow UUID '{target_uuid}' not found in DB.")
            finally:
                session_db.close()

            # Stop here. Do not process global triggers.
            return


        # --- 2. GLOBAL TRIGGERS (Priority Low) ---
        session = SessionLocal()
        try:
            # Check for triggers that are active AND are not "manual" states
            workflows = session.query(Workflow).filter(
                Workflow.trigger_event == "message",
                Workflow.is_active == True
            ).all()

            if not workflows: return

            for flow in workflows:
                data = flow.compiled_json
                if isinstance(data, str): data = json.loads(data)

                if data.get("filter"):
                    if not evaluate_condition(data["filter"], message):
                        continue

                print(f"🚀 Triggering New Workflow: {flow.name}")
                actions = data.get("actions", [])
                await execute_instructions(actions, message)

        except Exception as e:
            print(f"🔥 Runtime Error: {e}")
        finally:
            session.close()


async def setup(bot):
    await bot.add_cog(AutomationCog(bot))
