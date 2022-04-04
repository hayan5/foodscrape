import json
from typing import Any, List, Union

import bs4
from bs4 import BeautifulSoup

from foodscrape.common import Recipe
from foodscrape.ingredient import scrape_ingredient
from foodscrape.logger import get_logger

logger = get_logger(__name__)


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
    recipe_instructions = get_instructions(json_data["recipeInstructions"])
    recipe_ingredients = scrape_ingredient(soup)

    return Recipe(
        name=name,
        date_published=date_published,
        description=description,
        image=image,
        author=author,
        recipe_category=recipe_category,
        keywords=keywords,
        recipe_yield=recipe_yield,
        cook_time=cook_time,
        prep_time=prep_time,
        total_time=total_time,
        rating=rating,
        recipe_instructions=recipe_instructions,
        recipe_ingredients=recipe_ingredients,
    )


def get_meta_data(
    soup: BeautifulSoup,
) -> Union[bs4.element.Tag, bs4.element.NavigableString, None]:
    return soup.find("script", {"type": "application/ld+json"})


def get_instructions(json_list: Any) -> List[str]:
    instructions: List[str] = list()
    for i in json_list:
        instructions.append(i["text"])

    return instructions
