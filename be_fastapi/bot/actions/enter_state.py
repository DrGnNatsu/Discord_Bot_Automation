import discord

from bot.core.session_manager import create_or_update_session


async def enter_state(event: discord.Message, params):
    """
    Usage: ACTION: ENTER_STATE target="step_2_ban"
    """
    target_state_name = params.get("target")
    if not target_state_name:
        print("⚠️ ENTER_STATE missing target")
        return

    # In this logic, the 'target' is the NAME of the next workflow (e.g., 'step_2_ban')
    create_or_update_session(
        user_id=event.author.id,
        workflow_name=target_state_name,
        next_state="start" # usually we start at the beginning of the new flow
    )