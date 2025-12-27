import discord


def evaluate_condition(condition, event: discord.Message):
    """
    Evaluates JSON logic like: "message.content contains 'secret'"
    Returns True or False.
    """
    if not condition:
        return True

    # 1. Extract parts
    left_part = condition.get("left")  # e.g. "message.content" OR {"type": "variable", "name": "message.content"}
    op = condition.get("operator")  # e.g. "contains", "=="
    right_val = condition.get("right")  # e.g. "secret"

    # Handle Compiler Output (which wraps vars in dicts) vs Manual (strings)
    left_str = None
    if isinstance(left_part, dict) and left_part.get("type") == "variable":
        left_str = left_part.get("name")
    else:
        left_str = left_part

    # 2. Resolve the "left" side (The Variable)
    actual_value = None
    if left_str == "message.content":
        actual_value = event.content
    elif left_str == "author.id":
        actual_value = str(event.author.id)
    elif left_str == "channel.name":
        # Handle cases where channel might not have a name (e.g. DM)
        actual_value = getattr(event.channel, "name", "dm")

    # 3. Compare (The Operator)
    if op == "==": return actual_value == right_val
    if op == "!=": return actual_value != right_val
    if op == "contains": return right_val in (actual_value or "")

    return False
