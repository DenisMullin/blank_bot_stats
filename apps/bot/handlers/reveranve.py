from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.methods import SendMessage, DeleteMessage, SendDocument

from core.container import Container


router = Router()

@router.message(Command('start'))
async def reveranve(message: Message, container: Container) -> None:
    print("xmxmxmxm")