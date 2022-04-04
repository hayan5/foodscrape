from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, List, Literal, Tuple, Union

import pandas as pd
from bs4 import BeautifulSoup
from requests import Session


class ScrapedElement(ABC):
    @abstractmethod
    def to_dataframe(self) -> pd.DataFrame:
        pass


@dataclass
class Sitemap(ScrapedElement):
    urls: List[str] = field(default_factory=list)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.urls, columns=["url"])


@dataclass
class Ingredient(ScrapedElement):
    name: Union[List[Tuple[str, str]], Literal[""]]
    quantity: str
    original_text: str
    comments: str

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict([self.__dict__])


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

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict([self.__dict__])


ScrapeStrategyFunction = Callable[[BeautifulSoup], ScrapedElement]
ExportStrategyFunction = Callable[[ScrapedElement], Union[None, pd.DataFrame]]
FetchStrategyFunction = Callable[[str, Session], bytes]
