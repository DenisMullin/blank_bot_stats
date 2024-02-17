from database.models.metadata import metadata
from database.models.user import User

from databases import Database

from sqlalchemy.orm import Query
from sqlalchemy import Table

from .repository import Repository


class UserRepository(Repository[User]):
    model = User
    table: Table

    def __init__(self, database: Database):
        super().__init__(database)
        self.table = metadata.tables["user"]

    async def entry(
        self, id: int, first_name: str, last_name: str, username: str
    ) -> User | None:
        query: Query = self.table.insert().values(
            first_name=first_name, id=id, last_name=last_name, username=username
        ).returning(self.table)
        return self.to_model(await self.database.fetch_one(query=query))

    async def get_entry(self, id: int) -> User | None:
        query: Query = self.table.select().where(
            id == self.table.c.id
        )
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def update_first_name(
        self, id: int, first_name: str
    ) -> User | None:
        query: Query = (
            self.table
            .update()
            .where(id == self.table.c.id)
            .values(first_name=first_name)
            .returning(self.table)
        )
        
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def update_last_name(
        self, id: int, last_name: str
    ) -> User | None:
        query: Query = (
            self.table
            .update()
            .where(id == self.table.c.id)
            .values(last_name=last_name)
            .returning(self.table)
        )
        
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def update_username(
        self, id: int, username: str
    ) -> User | None:
        query: Query = (
            self.table
            .update()
            .where(id == self.table.c.id)
            .values(username=username)
            .returning(self.table)
        )
        
        return self.to_model(await self.database.fetch_one(query=query))