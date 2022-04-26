from flask_testing import TestCase

from foodscrape.app import create_app, db
from foodscrape.scrape.models import Sitemap


class TestSitemap(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_db(self):
        urls = [
            ("http://www.local.com", True, True),
            ("http://www.hello.org", True, False),
            ("http://testing123.com", True, False),
            ("http://foodcrape.com", False, True),
            ("http://www.sample.com", False, False),
        ]

        for url, ingredient_scraped, recipe_scraped in urls:
            sitemap = Sitemap(url=url)
            sitemap.ingredient_scraped = ingredient_scraped
            sitemap.recipe_scraped = recipe_scraped
            sitemap.save()

    def test_save(self):
        url = "http://www.localtest.com"
        sitemap = Sitemap(url=url)

        sitemap = sitemap.save()

        self.assertEqual(sitemap.url, url)

        url = sitemap.save()
        assert url is None

    def test_scrape_ingredient(self):
        url = "http://www.localtest.com"
        sitemap = Sitemap(url=url)
        sitemap = sitemap.save()

        sitemap = sitemap.scrape_ingredient()

        assert sitemap.ingredient_scraped is True

    def test_scrape_recipe(self):
        url = "http://www.localtest.com"
        sitemap = Sitemap(url=url)
        sitemap = sitemap.save()

        sitemap = sitemap.scrape_recipe()

        assert sitemap.recipe_scraped is True

    def test_get_ingredient_scraped(self):
        self.populate_db()
        sitemaps = Sitemap.get_ingredient_scraped(1)
        assert len(sitemaps) == 1

        sitemaps = Sitemap.get_ingredient_scraped(10)

        for sitemap in sitemaps:
            assert sitemap.ingredient_scraped is False

    def test_get_recipe_scraped(self):
        self.populate_db()
        sitemaps = Sitemap.get_recipe_scraped(1)
        assert len(sitemaps) == 1

        sitemaps = Sitemap.get_recipe_scraped(10)

        for sitemap in sitemaps:
            assert sitemap.recipe_scraped is False
