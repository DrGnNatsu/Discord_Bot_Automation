import discord

from bot.utils.time_converter import parse_duration


async def timeout_user(event: discord.Message, params: dict):
    """
    Timeouts the user for a specific duration.
    Usage: ACTION: TIMEOUT_USER duration="10m"
    """
    user = event.author
    duration_str = params.get("duration", "5m")
    duration_obj = parse_duration(duration_str)

    # Safety: Don't time out admins
    if user.guild_permissions.administrator:
        print(f"⚠️ Safety Prevented Timeout Admin: {user}")
        return

    try:
        await user.timeout(duration_obj, reason="GuildFlow Automated Timeout")
        print(f"⏳ Timed out {user} for {duration_str}")
    except discord.Forbidden:
        print(f"❌ Error: Bot lacks permission to timeout {user}")