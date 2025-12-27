import discord


def evaluate_condition(condition, event: discord.Message):
    """
    Evaluates JSON logic like: "message.content contains 'secret'"
    Returns True or False.
    """
    if not condition:
        return True

    # 1. Extract parts
    left_str = condition.get("left")  # e.g. "message.content"
    op = condition.get("operator")  # e.g. "contains", "=="
    right_val = condition.get("right")  # e.g. "secret"

    # 2. Resolve the "left" side (The Variable)
    actual_value = None
    if left_str == "message.content":
        actual_value = event.content
    elif left_str == "author.id":
        actual_value = str(event.author.id)
    elif left_str == "channel.name":
        actual_value = event.channel.name

    # 3. Compare (The Operator)
    if op == "==": return actual_value == right_val
    if op == "!=": return actual_value != right_val
    if op == "contains": return right_val in (actual_value or "")

    return False
