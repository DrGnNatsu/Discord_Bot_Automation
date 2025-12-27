import discord

from bot.core.session_manager import delete_session


async def exit_workflow(event: discord.Message, params: dict):
    """
    Removes the user from the active session.
    Usage: ACTION: EXIT_WORKFLOW
    """
    delete_session(event.author.id)