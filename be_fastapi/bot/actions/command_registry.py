from bot.actions.ban_user import ban_user
from bot.actions.reply_msg import reply_message
from bot.actions.send_msg import send_message
from bot.actions.timeout_user import timeout_user

COMMAND_MAP = {
    "SEND_MESSAGE": send_message,
    "REPLY_MESSAGE": reply_message,
    "BAN_USER": ban_user,
    "TIMEOUT_USER": timeout_user
}
