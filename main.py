import flask.helpers

from foodscrape.app import create_app
from foodscrape.config import DevConfig

CONFIG = DevConfig
print(flask.helpers.get_env())
app = create_app(CONFIG)  # type: ignore
