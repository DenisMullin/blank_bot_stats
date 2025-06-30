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

    async def update_button(self, id: int) -> User | None:
        query: Query = (
            self.table
            .update()
            .where(id == self.table.c.id)
            .values(sbp_pressed=True)
            .returning(self.table)
        )

        return self.to_model(await self.database.fetch_one(query=query))

    async def update_state(self, id: int, state: str) -> User | None:
        query: Query = (
            self.table
            .update()
            .where(id == self.table.c.id)
            .values(state=state)
            .returning(self.table)
        )

        return self.to_model(await self.database.fetch_one(query=query))

    async def update_styles(self, id, style: str) -> User | None:
        q: Query = self.table.select().where(
            id == self.table.c.id
        )
        record = await self.database.fetch_one(q)
        if not record:
            return None

        current_styles = record["styles"] or []
        if style not in current_styles:
            current_styles.append(style)

        query: Query = (
            self.table
            .update()
            .where(id == self.table.c.id)
            .values(styles=current_styles)
            .returning(self.table)
        )

        return self.to_model(await self.database.fetch_one(query=query))
