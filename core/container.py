from sqlalchemy.ext.asyncio import create_async_engine
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .singleton import Singleton
from .config import Settings

from database.repositories.user_repository import UserRepository


class BaseContainer:
    _database: Database | None = None
    _config: Settings

    _user_repository: UserRepository | None = None

    def __init__(self, config: Settings):
        self._config = config

    async def reconnect(self) -> None:
        if not self.database.is_connected:
            await self.database.connect()

    async def shutdown(self) -> None:
        if self.db.is_connected:
            await self.db.disconnect()

    @property
    def database(self) -> Database:
        if self._database is None:
            self._database = Database(self._config.DATABASE_URL)
        return self._database
    
    @property
    def config(self) -> Settings:
        return self._config
    
    @property
    def user_repository(self) -> UserRepository:
        if self._user_repository is None:
            self._user_repository = UserRepository(database=self.database)
        return self._user_repository


class Container(BaseContainer, metaclass=Singleton):
    pass


class DevContainer(BaseContainer):
    pass