from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.methods import SendMessage

from core.container import Container


router = Router()

@router.message(F.text.in_([__("/start")]))
async def reveranve(message: Message, container: Container, bot: Bot) -> None:
    projectName = (await bot.get_me()).full_name

    await bot(
        SendMessage(
            text=_("Project {}").format(projectName),
            chat_id=message.chat.id
        )
    )