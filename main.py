from foodscrape.app import create_app
from foodscrape.config import DevConfig

CONFIG = DevConfig

app = create_app(CONFIG)  # type: ignore
