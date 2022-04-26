import html
import json
from typing import Any, List, Union

import bs4
import requests
from bs4 import BeautifulSoup

from foodscrape.database import db
from foodscrape.fetch import fetch_data_uncompressed
from foodscrape.logger import get_logger

from .models import Instruction, Keyword, Recipe, Recipe_Ingredient
from .util import IngredientModel

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
    ingredients = scrape_ingredient(soup)

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

    # recipe_ingredients = []
    for ingredient in ingredients:
        # recipe_ingredients.append(ingredient)
        db.session.add(ingredient)

    recipe.instructions = recipe_instructions
    recipe.keywords = recipe_keywords
    recipe.ingredients = ingredients
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


def scrape_ingredient(soup: BeautifulSoup) -> List[Recipe_Ingredient]:
    ingredients: List[Recipe_Ingredient] = list()
    ingredient_elements = soup.find_all(
        "div", class_="recipe-ingredients__ingredient"
    )
    for element in ingredient_elements:
        quantity = get_quantity(element)
        original_text, names = parse_ingredient(element)

        ingredient = Recipe_Ingredient(
            ingredient_name=names[0][1],
            quantity=quantity,
            text=original_text,
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
