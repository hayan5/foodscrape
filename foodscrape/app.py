from typing import Any

from flask import Flask

from foodscrape import commands, recipe, sitemap
from foodscrape.config import ProdConfig
from foodscrape.extensions import db, migrate
from foodscrape.sitemap.models import Sitemap


def create_app(config_object: Any = ProdConfig):

    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_commands(app)
    register_blueprints(app)
    register_shellcontext(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)


def register_commands(app: Flask):
    app.cli.add_command(commands.test)


def register_shellcontext(app):
    def shell_context():
        return {"db": db, "Sitemap": Sitemap}

    app.shell_context_processor(shell_context)


def register_blueprints(app):
    app.register_blueprint(sitemap.views.blueprint)
    app.register_blueprint(recipe.views.blueprint)
