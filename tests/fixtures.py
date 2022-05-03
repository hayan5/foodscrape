import pytest

from foodscrape.app import create_app
from foodscrape.config import TestConfig
from foodscrape.extensions import db as _db
from foodscrape.scrape.models import (
    Ingredient,
    RecipeInstruction,
    RecipeKeyword,
    Sitemap,
)


@pytest.fixture(autouse=True)
def application():
    app = create_app(TestConfig)

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture()
def database():
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture
def sitemap_not_scraped(database):

    sitemap = Sitemap(url="http://sitemap_not_scraped.com")
    sitemap.save()
    return sitemap


@pytest.fixture
def ingredient(database):
    ingredient = Ingredient("chicken")
    return ingredient.save()


@pytest.fixture
def ingredients(database):
    ingredients = [("chicken", 3), ("bread", 5), ("rice", 1)]

    for name, times in ingredients:
        for i in range(times):
            ingredient = Ingredient(name=name)
            ingredient.save()


@pytest.fixture
def keywords(database):
    keyword_models = []
    keyword_list = ["fun", "quick", "easy", "30min"]
    for keyword in keyword_list:
        keyword_model = RecipeKeyword(keyword)
        keyword_models.append(keyword_model)

    return keyword_models


@pytest.fixture
def instructions(database):
    instruction_models = []
    instruction_list = [
        "instruction 1",
        "instruction 2",
        "instruction 3",
        "instruction 4",
    ]
    for i, instruction in enumerate(instruction_list):
        instruction_model = RecipeInstruction(i, instruction)
        instruction_models.append(instruction_model)

    return instruction_models
