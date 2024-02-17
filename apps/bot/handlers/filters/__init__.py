from aiogram.filters import Filter
from aiogram.types import Message


class GetMessage(Filter):
    def __init__(self, msg: str | list) -> None:
        self.msg = msg

    async def __call__(self, message: Message) -> bool:
        return ((message.text == self.msg) | (message.text in self.msg))