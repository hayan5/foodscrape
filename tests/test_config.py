from flask_testing import TestCase

from foodscrape.app import create_app
from foodscrape.config import DevConfig


class TestDevConfig(TestCase):
    def create_app(self):
        return create_app(DevConfig)

    def test_app_is_dev(self):
        app = self.create_app()
        self.assertTrue(app.config["DEBUG"] is True)
