import json
from typing import Any, List, Union

import bs4
import requests
from bs4 import BeautifulSoup

from foodscrape.database import db
from foodscrape.fetch import fetch_data_uncompressed
from foodscrape.logger import get_logger

from .models import Ingredient, Instruction, Keyword, Recipe

logger = get_logger(__name__)


def get_data(url: str):
    session = requests.Session()
    data = fetch_data_uncompressed(url, session)
    soup = BeautifulSoup(data, "lxml")
    recipe = scrape_recipe(soup)
    return recipe


def scrape_recipe(soup: BeautifulSoup) -> Recipe:
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
    ingredients = json_data["recipeIngredient"]

    # for i in recipe_ingredients:
    #     logger.info(i)

    recipe = Recipe(
        name=name,
        date_published=date_published,
        description=description,
        image=image,
        author=author,
        recipe_category=recipe_category,
        recipe_yield=recipe_yield,
        cook_time=cook_time,
        prep_time=prep_time,
        total_time=total_time,
        rating=rating,
    )

    db.session.add(recipe)
    recipe_keywords = []
    for keyword in keywords:
        keyword_model = Keyword(text=keyword)
        recipe_keywords.append(keyword_model)
        db.session.add(keyword_model)

    recipe_instructions = []
    i = 1
    for instruction in instructions:
        instruction_model = Instruction(text=instruction, seq_num=i)
        recipe_instructions.append(instruction_model)
        db.session.add(instruction_model)
        i += 1

    recipe_ingredients = []
    for ingredient in ingredients:
        ingredient_model = Ingredient(text=ingredient)
        recipe_ingredients.append(ingredient_model)
        db.session.add(ingredient_model)

    recipe.instructions = recipe_instructions
    recipe.keywords = recipe_keywords
    recipe.ingredients = recipe_ingredients
    db.session.commit()

    return recipe


def get_meta_data(
    soup: BeautifulSoup,
) -> Union[bs4.element.Tag, bs4.element.NavigableString, None]:
    return soup.find("script", {"type": "application/ld+json"})


def get_instructions(json_list: Any) -> List[str]:
    instructions: List[str] = list()
    for i in json_list:
        instructions.append(i["text"])

    return instructions
