import os


class Config:
    SECRET_KEY = os.getenv("FOODSCRAPE_SECRET", "secret-key")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGGER_FORMAT = (
        "[%(asctime)s] [%(levelname)s] %(name)s %(funcName)s :: "
        + "%(message)s"
    )


class ProdConfig(Config):
    ENV = "prod"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:password@127.0.0.1:5433/foodscrape",
    )


class DevConfig(Config):
    ENV = "dev"
    DEBUG = True
    DB_NAME = "dev.db"

    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(DB_PATH)


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
