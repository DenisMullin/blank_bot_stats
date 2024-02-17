from databases import Database
from databases.backends.postgres import Record

import typing as tp


T = tp.TypeVar("T")


class Repository(tp.Generic[T]):
    database: Database
    model: T

    def __init__(self, database: Database):
        self.database = database

    def to_model(self, record: Record | None) -> T | None:
        if record is None:
            return None

        row = dict(record._mapping.items())
        return self.model(**row)

    def to_models(self, records: tp.List[Record]) -> tp.List[T]:
        return [self.to_model(rec) for rec in records]
