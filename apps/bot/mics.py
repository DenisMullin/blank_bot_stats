from aiogram.types import TelegramObject
from pathlib import Path

from exceptions.exceptions import RegistrationError
from database.models.user import User
from core.container import Container


path = Path(__file__).parent

async def registr(
    event_from_user: TelegramObject, _user: User, container: Container
) -> None:
    if (_user):
        if not (_user.first_name is event_from_user.first_name):
            await container.user_repository.update_first_name(
                event_from_user.id, event_from_user.first_name
            )
        if not (_user.last_name is event_from_user.last_name):
            await container.user_repository.update_last_name(
                event_from_user.id, event_from_user.last_name
            )
        if not (_user.username is event_from_user.username):
            await container.user_repository.update_username(
                event_from_user.id, event_from_user.username
            )
    else:
        registr = await container.user_repository.entry(
            event_from_user.id, event_from_user.first_name, event_from_user.last_name, event_from_user.username
        )

        if not registr:
            raise RegistrationError