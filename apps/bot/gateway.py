from aiogram.utils.i18n import FSMI18nMiddleware, I18n
from aiogram.types import TelegramObject, User
from aiogram import Dispatcher, Bot, Router
from aiogram.fsm.storage.memory import MemoryStorage

from typing import Callable, Dict, Any, Awaitable

from .handlers import handlers
from .mics import path, registr

from core.config import settings, project_folder
from core.container import Container


class Gateway():
    def __init__(
            self, container: Container, handlers: list[Router]
        ) -> None:
        self.container = container

        self.bot = Bot(token=container.config.BOT_TOKEN)
        self.dispatcher = Dispatcher(storage=MemoryStorage())

        lazy = I18n(
            path=path / "locales", default_locale="en", domain="messages"
        )
        self.dispatcher.message.outer_middleware(
            FSMI18nMiddleware(lazy)
        )
        self.dispatcher.callback_query.outer_middleware(
            FSMI18nMiddleware(lazy)
        )

        for handler in handlers:
            self.dispatcher.include_router(handler)

        @self.dispatcher.update.outer_middleware()
        async def extentions(
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
        ) -> None:
            event_from_user: User = data['event_from_user']
            _user = await container.user_repository.get_entry(
                event_from_user.id
            )
            await registr(event_from_user, _user, container)

            data["container"] = container
            await handler(event, data)

    async def host(self) -> None:
        await self.container.reconnect()
        
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dispatcher.start_polling(
            self.bot, allowed_updates=self.dispatcher.resolve_used_update_types()
        )

        await self.container.shutdown()


gateway = Gateway(container=Container(settings), handlers=handlers)