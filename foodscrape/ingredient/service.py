import html

import requests
from bs4 import BeautifulSoup

from foodscrape.database import db
from foodscrape.fetch import fetch_data_uncompressed

from .models import RawIngredient


def scrape_url(url: str):

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

            raw_ingredient = RawIngredient(name=ingredient)
            ingredients.append(raw_ingredient)
            db.session.add(raw_ingredient)

    db.session.commit()
    return ingredients


def proccess_text(text: str) -> str:
    text = html.unescape(text)
    text = " ".join(text.split())
    return text
