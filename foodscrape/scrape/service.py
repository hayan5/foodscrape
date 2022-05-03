import html
import json
from typing import Any, List, Union

import bs4
from bs4 import BeautifulSoup, Tag
from requests import Session
from sqlalchemy import func, select

from foodscrape.database import session
from foodscrape.fetch import fetch_data_compressed, fetch_data_uncompressed
from foodscrape.logger import get_logger

from .exceptions import FoodScrapeError
from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeInstruction,
    RecipeKeyword,
    Sitemap,
)
from .util import IngredientModel

# from sqlalchemy.orm import


logger = get_logger(__name__)


def scrape_sitemap_from_url(url: str):
    session = Session()
    data = fetch_data_compressed(url, session=session)
    soup = BeautifulSoup(data, "lxml")
    sitemaps = []
    for element in soup.find_all("loc"):
        try:
            url = _get_sitemap_url(element)
            sitemap = Sitemap(url=url)
            sitemaps.append(sitemap.save())

        except FoodScrapeError as e:
            logger.debug(e)
            continue

    session.close()
    logger.info("Sitemap Successfully Saved")


def _get_sitemap_url(element) -> str:
    if isinstance(element, Tag):
        url = element.text.strip()
        return url


def scrape_ingredients(limit: int) -> List[List[Ingredient]]:
    sitemaps_to_scrape = Sitemap.get_ingredient_scraped(limit)
    logger.info(sitemaps_to_scrape.__repr__())
    session = Session()

    all_found_ingredients = []

    for sitemap in sitemaps_to_scrape:
        logger.info(sitemap.url)
        data = fetch_data_uncompressed(sitemap.url, session=session)
        soup = BeautifulSoup(data, "lxml")

        saved_ingredients = []
        ingredients = _find_ingredients(soup)
        for ingredient in ingredients:
            saved_ingredients.append(ingredient.save())

        all_found_ingredients.append(saved_ingredients)

    return all_found_ingredients


def _find_ingredients(soup: BeautifulSoup) -> List[Ingredient]:
    elements = soup.findAll(
        "span", class_="recipe-ingredients__ingredient-part"
    )

    ingredients = []
    for element in elements:
        children = element.findChildren("a", recursive=False)

        for child in children:
            ingredient = _proccess_ingredient(child.text)

            raw_ingredient = Ingredient(name=ingredient)
            ingredients.append(raw_ingredient)

    return ingredients


def _proccess_ingredient(text: str) -> str:
    text = html.unescape(text)
    text = " ".join(text.split())
    return text


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


def scrape_recipes(limit: int) -> List[Recipe]:
    recipes_to_scrape = Sitemap.get_recipe_scraped(limit)
    recipes = []
    for recipe in recipes_to_scrape:
        recipe.scrape_recipe()
        recipes.append(scrape_recipe(recipe.url))

    return recipes


def scrape_recipe(url: str) -> Recipe:
    session = Session()
    data = fetch_data_uncompressed(url, session=session)
    soup = BeautifulSoup(data, "lxml")
    json_data = get_meta_data(soup)
    if json_data is None:
        raise Exception

    json_data = json.loads(json_data.getText())
    name = json_data["name"]
    date_published = json_data["datePublished"]
    description = json_data["description"]
    image = json_data["image"]
    author = json_data["author"]
    recipe_category = json_data["recipeCategory"]
    keywords = json_data["keywords"].split(",")
    recipe_yield = json_data["recipeYield"]
    cook_time = json_data["cookTime"]
    prep_time = json_data["prepTime"]
    total_time = json_data["totalTime"]
    rating = json_data["aggregateRating"]["ratingValue"]
    instructions = get_instructions(json_data["recipeInstructions"])
    ingredients = scrape_ingredient(soup)

    recipe = Recipe(name=name)
    recipe.date_published = date_published
    recipe.description = description
    recipe.image = image
    recipe.author = author
    recipe.recipe_category = recipe_category
    recipe.recipe_yield = recipe_yield
    recipe.cook_time = cook_time
    recipe.prep_time = prep_time
    recipe.total_time = total_time
    recipe.rating = rating

    recipe_keywords = []
    for keyword in keywords:
        keyword_model = RecipeKeyword(text=keyword)
        recipe_keywords.append(keyword_model)

    recipe_instructions = []
    i = 1
    for instruction in instructions:
        instruction_model = RecipeInstruction(text=instruction, seq_num=i)
        recipe_instructions.append(instruction_model)
        i += 1

    recipe_ingredients = []
    for ingredient in ingredients:
        pass
        recipe_ingredients.append(ingredient)
        # db.session.add(ingredient)

    recipe.instructions = recipe_instructions
    recipe.keywords = recipe_keywords
    recipe.ingredients = recipe_ingredients

    logger.info([i.__repr__() for i in recipe_ingredients])

    return recipe.save()


def get_meta_data(
    soup: BeautifulSoup,
) -> Union[bs4.element.Tag, bs4.element.NavigableString, None]:
    return soup.find("script", {"type": "application/ld+json"})


def get_instructions(json_list: Any) -> List[str]:
    instructions: List[str] = list()
    for i in json_list:
        instructions.append(i["text"])

    return instructions


def scrape_ingredient(soup: BeautifulSoup) -> List[RecipeIngredient]:
    ingredients: List[RecipeIngredient] = list()
    ingredient_elements = soup.find_all(
        "div", class_="recipe-ingredients__ingredient"
    )
    for element in ingredient_elements:
        quantity = get_quantity(element)
        original_text, names = parse_ingredient(element)
        if names == []:
            names = ""
        else:
            names = names[-1]
        ingredient = RecipeIngredient(
            ingredient_name=names,
            quantity=quantity,
            original_text=original_text,
        )

        ingredients.append(ingredient)

    return ingredients


def parse_ingredient(element):
    ingredient_parts_element = element.find(
        "div", class_="recipe-ingredients__ingredient-parts"
    )
    names = ""
    original_text = ""

    if isinstance(ingredient_parts_element, bs4.element.Tag):
        text = scrape_ingredient_parts(ingredient_parts_element)
        original_text = text
        names = IngredientModel.find_ingredients(text)
        logger.info(names)

    return (original_text, names)


def scrape_ingredient_parts(ingredient_parts_element: bs4.element.Tag):
    return parse_text(ingredient_parts_element.getText())


def parse_text(text: str) -> str:
    text = html.unescape(text)
    text = " ".join(text.split())
    return text


def get_text(ingredient_element) -> str:
    text = ingredient_element.getText()
    text = html.unescape(text)
    text = " ".join(text.split())
    return text


def get_quantity(ingredient_element) -> str:
    quantity: str = ""

    quantity_element = ingredient_element.find(
        "div", class_="recipe-ingredients__ingredient-quantity"
    )

    if isinstance(quantity_element, bs4.element.Tag):
        quantity = quantity_element.getText()
        quantity = quantity.replace("\u2044", "/")
        quantity = html.unescape(quantity)
        quantity = quantity.replace(" -", "-")
        quantity = " ".join(quantity.split())
        quantity = quantity.replace(" -", " - ")
        quantity = quantity.replace("- ", " - ")

    return quantity
