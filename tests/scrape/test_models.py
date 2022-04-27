from flask_testing import TestCase

from foodscrape.app import create_app, db
from foodscrape.scrape.models import Ingredient, Sitemap


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


class TestIngredient(TestCase):
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
        ingredients = [("chicken", 3), ("bread", 5), ("rice", 1)]

        for name, times in ingredients:
            for i in range(times):
                ingredient = Ingredient(name=name)
                ingredient.save()

    def test_save(self):
        ingredient = Ingredient("chicken")
        result = ingredient.save()

        assert result.name == "chicken"
        assert result.times_seen == 1

        ingredient = Ingredient("chicken")
        result = ingredient.save()

        assert result.name == "chicken"
        assert result.times_seen == 2

    def test_get_seen_greater_than_or_eq(self):
        self.populate_db()

        ingredients = Ingredient.get_seen_greater_than_or_eq(3)

        for ingredient in ingredients:
            assert ingredient.times_seen >= 3

    def test_get_seen_less_than_or_eq(self):
        self.populate_db()

        ingredients = Ingredient.get_seen_less_than_or_eq(3)

        for ingredient in ingredients:
            assert ingredient.times_seen <= 3
