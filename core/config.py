from dataclasses import dataclass
from dotenv import load_dotenv
import sentry_sdk
from os import path, environ

from .singleton import Singleton


project_folder = path.dirname(path.dirname(path.abspath(__file__)))
load_dotenv(path.join(project_folder, ".env"))

@dataclass(frozen=True)
class Settings(metaclass=Singleton):
    SENTRY_DSN: str = environ.get("SENTRY_DSN")

    DATABASE_URL: str = environ.get("DATABASE_URL")

    BOT_TOKEN: str = environ.get("BOT_TOKEN")
    
    def __init__(self):
        if len(self.SENTRY_DSN) > 0:
            sentry_sdk.init(dsn=self.SENTRY_DSN, traces_sample_rate=1.0)


settings = Settings()