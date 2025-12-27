# --- HELPER 2: The Recursive Dispatcher ---
import discord

from bot.actions.command_registry import COMMAND_MAP
from bot.utils.logic_evaluator import evaluate_condition


async def execute_instructions(actions_list, event: discord.Message):
    """
    Iterates through the JSON list and executes actions.
    Supports Recursion for 'LOGIC_IF' blocks.
    """
    for step in actions_list:
        step_type = step.get("type")

        # CASE A: Standard Action (e.g., SEND_MESSAGE)
        if step_type == "ACTION":
            cmd_name = step.get("command")
            params = step.get("params", {})

            # Find the function in your actions.py MAP
            func = COMMAND_MAP.get(cmd_name)
            if func:
                print(f"   ▶ Executing {cmd_name}...")
                try:
                    await func(event, params)
                except Exception as e:
                    print(f"   ❌ Error running {cmd_name}: {e}")
            else:
                print(f"   ⚠ Unknown command: {cmd_name}")

        # CASE B: Logic Branch (Recursion)
        elif step_type == "LOGIC_IF":
            condition = step.get("condition")
            # Evaluate: If True, run the 'body'
            if evaluate_condition(condition, event):
                print(f"   🤔 Condition matched. Entering IF block.")
                await execute_instructions(step.get("body", []), event)
            else:
                # Optional: Run 'else_body'
                else_body = step.get("else_body", [])
                if else_body:
                    print(f"   🤔 Condition failed. Entering ELSE block.")
                    await execute_instructions(else_body, event)
