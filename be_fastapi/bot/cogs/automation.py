import json
import logging
import traceback

import discord
from discord.ext import commands

from app.db.session import SessionLocal
from app.models import Workflow
from bot.core.session_manager import get_user_session, clear_all_sessions
from bot.utils.logic_evaluator import evaluate_condition
from bot.utils.recursive_dispatcher import execute_instructions

logger = logging.getLogger(__name__)


class AutomationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return

        # --- 0. SAFETY NET & RESTART COMMAND ---
        try:
            # 1. EMERGENCY RESET COMMAND (Administrator Only)
            if message.content == "!reset" and message.author.guild_permissions.administrator:
                try:
                    count = clear_all_sessions()
                    await message.channel.send(f"🧹 **System Reset:** All {count} active sessions cleared.")
                    print("🧹 [ADMIN] System Reset Triggered")
                except Exception as e:
                    print(f"🔴 [ERROR] Reset failed: {e}")
                return

            # Demo Log
            print(f"🔵 [INFO] Message from {message.author.name}")

            # --- 2. CHECK FOR ACTIVE SESSION (Priority High) ---
            user_session = get_user_session(message.author.id)

            if user_session:
                # FIX: We use the 'workflow_id' (UUID) to find the logic, NOT the 'current_state' string.
                target_uuid = user_session.workflow_id
                
                # Demo Log
                print(f"🔎 [DB] Found active session. Workflow UUID: {target_uuid}")

                session_db = SessionLocal()
                try:
                    state_flow = session_db.query(Workflow).filter(
                        Workflow.id == target_uuid
                    ).first()

                    if state_flow:
                        data = state_flow.compiled_json
                        if isinstance(data, str): data = json.loads(data)

                        print(f"🟢 [EXEC] Resuming Workflow: {state_flow.name}")
                        # Support both 'steps' (Compiler) and 'actions' (Manual Seed)
                        actions = data.get("steps") or data.get("actions", [])
                        await execute_instructions(actions, message)
                    else:
                        print(f"🔴 [ERROR] Critical: Workflow UUID '{target_uuid}' not found.")
                finally:
                    session_db.close()

                # Stop here. Do not process global triggers.
                return


            # --- 3. GLOBAL TRIGGERS (Priority Low) ---
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

                    print(f"🟢 [EXEC] Triggering (Global): {flow.name}")
                    # Support both 'steps' (Compiler) and 'actions' (Manual Seed)
                    actions = data.get("steps") or data.get("actions", [])
                    await execute_instructions(actions, message)

            except Exception as e:
                print(f"🔴 [ERROR] Global Trigger Logic: {e}")
                traceback.print_exc()
            finally:
                session.close()

        except Exception as e:
            # SAFETY NET CATCH-ALL
            print(f"🔴 [ERROR] Runtime Exception detected! Bot prevented from crashing.")
            print(f"🔴 [ERROR] {str(e)}")
            traceback.print_exc()


async def setup(bot):
    await bot.add_cog(AutomationCog(bot))
