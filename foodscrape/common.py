from abc import ABC
from dataclasses import dataclass, field
from typing import Callable, List, Literal, Tuple, Union

from bs4 import BeautifulSoup
from requests import Session


class ScrapedElement(ABC):
    def __init__(self):
        raise NotImplementedError


@dataclass
class Sitemap(ScrapedElement):
    urls: List[str] = field(default_factory=list)


@dataclass
class Ingredient(ScrapedElement):
    name: Union[List[Tuple[str, str]], Literal[""]]
    quantity: str
    original_text: str
    comments: str


@dataclass
class Recipe(ScrapedElement):
    name: str
    date_published: str
    description: str
    image: str
    author: str
    recipe_category: str
    keywords: List[str]
    recipe_yield: str
    cook_time: str
    prep_time: str
    total_time: str
    rating: str
    recipe_instructions: List[str]
    recipe_ingredients: List[Ingredient] = field(default_factory=list)


ScrapeStrategyFunction = Callable[[BeautifulSoup], ScrapedElement]
ExportStrategyFunction = Callable[[ScrapedElement], None]
FetchStrategyFunction = Callable[[str, Session], bytes]
