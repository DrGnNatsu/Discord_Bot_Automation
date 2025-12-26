import discord


async def send_message(event: discord.Message, params: dict):
    """
    Sends a message to a specific channel.
    Usage: ACTION: SEND_MESSAGE channel="general" content="Hello"
    """
    guild = event.guild
    target_channel_id = params.get("channel")
    content = params.get("content")

    if not target_channel_id or not content:
        print("❌ Error: Missing channel or content for SEND_MESSAGE")
        return

    # 1. Try to find channel by Name
    channel = discord.utils.get(guild.text_channels, name=str(target_channel_id))

    # 2. If not found, try to find by ID
    if not channel:
        try:
            channel = guild.get_channel(int(target_channel_id))
        except ValueError:
            pass

    if channel:
        await channel.send(content)
        print(f"✅ Sent message to #{channel.name}")
    else:
        print(f"❌ Could not find channel: {target_channel_id}")