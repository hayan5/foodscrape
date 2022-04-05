import logging
import pathlib
from dataclasses import dataclass, field


@dataclass
class Paths:
    log: str
    data: str
    model: str


@dataclass
class Logger:
    format: str
    level: int


# host=127.0.0.1
# port=5432
# database=web_scraper
# user=postgres
# password=postgres
@dataclass
class Database:
    host: str = field(default="127.0.0.1")
    port: str = field(default="5433")
    database: str = field(default="foodscrape")
    user: str = field(default="harrisonayan")
    password: str = field(default="password")


@dataclass
class AConfig:
    paths: Paths
    logger: Logger
    db: Database
    debug: bool = False
    testing: bool = False


@dataclass
class AppConfig:
    # sitemap_url: str = "https://www.food.com/sitemap.xml"
    BASE_DIR: pathlib.Path = field(default=pathlib.Path.cwd(), init=False)
    DATA_DIR: pathlib.Path = field(init=False)
    LOGGER_DIR: pathlib.Path = field(init=False)
    MODEL_DIR: pathlib.Path = field(init=False)
    LOGGER_FORMAT: str = field(
        default="[%(asctime)s] [%(levelname)s] %(name)s %(funcName)s :: %(message)s",
    )
    LOGGER_LEVEL: int = field(default=logging.INFO)
    DB: Database = field(default=Database())

    def __post_init__(self) -> None:
        self.LOGGER_DIR = self.BASE_DIR / "logs"
        self.DATA_DIR = self.BASE_DIR / "data"
        self.MODEL_DIR = self.BASE_DIR / "models"

        if not self.LOGGER_DIR.is_dir():
            self.LOGGER_DIR.mkdir()
        if not self.DATA_DIR.is_dir():
            self.DATA_DIR.mkdir()
        if not self.MODEL_DIR.is_dir():
            self.MODEL_DIR.mkdir()


Config = AppConfig()
