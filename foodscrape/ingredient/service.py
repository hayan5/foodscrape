import html
from typing import List

import requests
from bs4 import BeautifulSoup

from foodscrape.database import db
from foodscrape.fetch import fetch_data_uncompressed

from .models import Ingredient


def find_ingredients_from_url(url: str) -> List[Ingredient]:

    session = requests.Session()
    data = fetch_data_uncompressed(url, session)
    soup = BeautifulSoup(data, "lxml")

    elements = soup.findAll(
        "span", class_="recipe-ingredients__ingredient-part"
    )

    ingredients = []
    for element in elements:
        children = element.findChildren("a", recursive=False)

        for child in children:
            ingredient = proccess_text(child.text)

            raw_ingredient = Ingredient(name=ingredient)
            ingredients.append(raw_ingredient)

    save_ingredients(ingredients)
    return ingredients


def save_ingredients(ingredients: List[Ingredient]) -> None:
    for ingredient in ingredients:
        ingredient_name = ingredient.name
        if does_ingredient_exist(ingredient_name) is False:
            db.session.add(ingredient)

    db.session.commit()


def does_ingredient_exist(ingredient_name: str) -> bool:
    q = db.session.query(Ingredient).filter(Ingredient.name == ingredient_name)
    if q.count() == 0:
        return False

    ingredient: Ingredient = q.first()
    ingredient.times_seen += 1

    return True


def proccess_text(text: str) -> str:
    text = html.unescape(text)
    text = " ".join(text.split())
    return text
