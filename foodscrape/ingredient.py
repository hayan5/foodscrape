import html
from typing import List

import bs4
from bs4 import BeautifulSoup

from foodscrape.common import Ingredient
from foodscrape.logger import get_logger
from foodscrape.models.ingredient import IngredientModel

logger = get_logger(__name__)


def scrape_ingredient(soup: BeautifulSoup) -> List[Ingredient]:
    ingredients: List[Ingredient] = list()
    ingredient_elements = soup.find_all("div", class_="recipe-ingredients__ingredient")
    for element in ingredient_elements:
        quantity = get_quantity(element)
        original_text, names = parse_ingredient(element)

        ingredient = Ingredient(
            name=names, quantity=quantity, original_text=original_text, comments=""
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
