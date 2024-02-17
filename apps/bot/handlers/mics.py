from aiogram.methods import SendMessage
from aiogram import Router, Bot
from aiogram.types import Message

from .filters import GetMessage


router = Router()

@router.message(GetMessage(['/hexGetChat/']))
async def hexGetChat(message: Message, bot: Bot) -> None:
    await bot(
        SendMessage(
            text="<b>Chat ID:</b> <code>{}</code>".format(message.chat.id),
            parse_mode="HTML",
            chat_id=message.chat.id
        )
    )