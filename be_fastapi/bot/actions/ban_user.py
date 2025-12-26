import discord


async def ban_user(event: discord.Message, params: dict):
    """
    Bans the user who sent the message.
    Usage: ACTION: BAN_USER
    """
    user = event.author

    # Safety: Don't ban the bot owner or admins
    if user.guild_permissions.administrator:
        print(f"⚠️ Safety Prevented Banning Admin: {user}")
        return

    try:
        await user.ban(reason="GuildFlow Automated Ban")
        print(f"🔨 Banned User: {user}")
    except discord.Forbidden:
        print(f"❌ Error: Bot lacks permission to ban {user}")