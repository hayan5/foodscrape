import pytest
from flask_testing import TestCase

from foodscrape.app import create_app, db
from foodscrape.logger import get_logger
from foodscrape.scrape.exceptions import FoodScrapeError
from foodscrape.scrape.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeInstruction,
    RecipeKeyword,
    Sitemap,
)

logger = get_logger(__name__)


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

    def test_sitemap_recipe_save(self):
        url = "http://www.localtest.com"

        sitemap1 = Sitemap(url=url)
        sitemap2 = Sitemap(url=url)

        saved_sitemap = sitemap1.save()

        assert saved_sitemap.url == url

        with pytest.raises(FoodScrapeError):
            sitemap2.save()

    def test_sitemap_scrape_ingredient(self):
        url = "http://www.localtest.com"
        sitemap = Sitemap(url=url)
        sitemap = sitemap.save()

        sitemap = sitemap.scrape_ingredient()

        assert sitemap.ingredient_scraped is True

    def test_sitemap_scrape_recipe(self):
        url = "http://www.localtest.com"
        sitemap = Sitemap(url=url)
        sitemap = sitemap.save()

        sitemap = sitemap.scrape_recipe()

        assert sitemap.recipe_scraped is True

    def test_sitemap_get_ingredient_scraped(self):
        self.populate_db()
        sitemaps = Sitemap.get_ingredient_scraped(1)
        assert len(sitemaps) == 1

        sitemaps = Sitemap.get_ingredient_scraped(10)

        for sitemap in sitemaps:
            assert sitemap.ingredient_scraped is False

    def test_sitemap_get_recipe_scraped(self):
        self.populate_db()
        sitemaps = Sitemap.get_recipe_scraped(1)
        assert len(sitemaps) == 1

        sitemaps = Sitemap.get_recipe_scraped(10)

        for sitemap in sitemaps:
            assert sitemap.recipe_scraped is False


def test_ingredient_save(database):
    ingredient = Ingredient("chicken")
    result = ingredient.save()

    assert result.name == "chicken"
    assert result.times_seen == 1

    ingredient = Ingredient("chicken")
    result = ingredient.save()

    assert result.name == "chicken"
    assert result.times_seen == 2


def test_ingredient_get_seen_greater_than_or_eq(ingredients):
    ingredients = Ingredient.get_seen_greater_than_or_eq(3)

    for ingredient in ingredients:
        assert ingredient.times_seen >= 3


def test_ingredient_get_seen_less_than_or_eq(ingredients):
    ingredients = Ingredient.get_seen_less_than_or_eq(3)

    for ingredient in ingredients:
        assert ingredient.times_seen <= 3


def test_recipe_save(keywords, instructions):
    i1 = Ingredient("Chicken")
    i2 = Ingredient("Rice")
    i1 = i1.save()
    i2 = i2.save()

    recipe_ingredients = [
        RecipeIngredient("1", "Chicken", ""),
        RecipeIngredient("2", "Rice", ""),
    ]
    recipe_ingredients[0].ingredient_id = i1.id
    recipe_ingredients[1].ingredient_id = i2.id

    recipe = Recipe(
        "Chicken and Rice",
        keywords=keywords,
        instructions=instructions,
        ingredients=recipe_ingredients,
    )

    result = recipe.save()

    assert result.name == recipe.name
    assert result.keywords == keywords
    assert result.instructions == instructions
    assert result.ingredients == recipe_ingredients


def test_recipe_delete(database, instructions):
    keywords = [
        RecipeKeyword("Fun"),
        RecipeKeyword("Easy"),
        RecipeKeyword("Quick"),
    ]
    recipe1 = Recipe(
        "Chicken and Rice", keywords=list(keywords), instructions=instructions
    )
    recipe2 = Recipe("Quesadilla", keywords=list(keywords))

    recipe1.keywords.append(RecipeKeyword("Recipe 1 Keyword"))
    recipe2.keywords.append(RecipeKeyword("Recipe 2 Keyword"))

    res1 = recipe1.save()
    res2 = recipe2.save()

    assert len(res1.keywords) == 4
    assert len(res2.keywords) == 4
    assert len(res1.instructions) == 4

    db.session.delete(res1)

    assert len(res1.keywords) == 4

    instructions = RecipeInstruction.get_all()
    assert len(instructions) == 0


def test_ingredients_query(database):
    ingredient1 = Ingredient("Chicken")
    ingredient2 = Ingredient("Rice")
    ingredient3 = Ingredient("Cheese")
    ingredient4 = Ingredient("Quesadilla")

    ingredient1.save()
    ingredient2.save()
    ingredient3.save()
    ingredient4.save()

    i = Ingredient.get_all_by_name(["chicken", "Rice"])

    assert len(i) == 2
