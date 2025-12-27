import discord


async def reply_message(event: discord.Message, params: dict):
    """
    Replies to the user who triggered the event.
    Usage: ACTION: REPLY_MESSAGE content="Hello there"
    """
    content = params.get("content")
    if content:
        # reference=event creates a "Reply" in Discord UI
        await event.channel.send(content, reference=event)
        print(f"✅ Replied to {event.author}")