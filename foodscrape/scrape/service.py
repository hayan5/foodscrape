from bs4 import BeautifulSoup, Tag
from requests import Session
from sqlalchemy import func, select

from foodscrape.database import session
from foodscrape.fetch import fetch_data_compressed
from foodscrape.logger import get_logger

from .exceptions import FoodScrapeError
from .models import Recipe, RecipeIngredient, Sitemap

# from sqlalchemy.orm import


logger = get_logger(__name__)


def scrape_sitemap_from_url(url: str):
    session = Session()
    data = fetch_data_compressed(url, session=session)
    soup = BeautifulSoup(data, "lxml")
    for element in soup.find_all("loc"):
        try:
            url = _get_sitemap_url(element)
            sitemap = Sitemap(url=url)
            return sitemap.save()

        except FoodScrapeError as e:
            logger.debug(e)
            continue

    session.close()
    logger.info("Sitemap Successfully Saved")


def _get_sitemap_url(element) -> str:
    if isinstance(element, Tag):
        url = element.text.strip()
        return url


def get_recipes_by_ingredients(names):
    names = [str.lower(name) for name in names]
    count = func.count()

    ingredients_searched = (
        select(RecipeIngredient.recipe_id, count)
        .where(func.lower(RecipeIngredient.ingredient_name).in_(names))
        .group_by(RecipeIngredient.recipe_id)
    ).subquery()

    possible_recipes = (
        select(RecipeIngredient.recipe_id, count).group_by(
            RecipeIngredient.recipe_id
        )
    ).subquery()

    matched_recipes = (
        select(possible_recipes, ingredients_searched)
        .filter(
            possible_recipes.c.recipe_id == ingredients_searched.c.recipe_id
        )
        .filter(possible_recipes.c.count == ingredients_searched.c.count)
    ).subquery()

    stmt = select(Recipe).filter(Recipe.id == matched_recipes.c.recipe_id)

    return session.execute(stmt).scalars()
