from __future__ import annotations

from typing import List

from sqlalchemy import Column, ForeignKey, Table, func, select
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Integer, String

from foodscrape.database import Base, session
from foodscrape.extensions import db
from foodscrape.logger import get_logger

from .exceptions import FoodScrapeError

logger = get_logger(__name__)


"""
    ------------Sitemap Tables------------
"""


class Sitemap(Base):
    __tablename__ = "sitemap"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)

    ingredient_scraped = Column(Boolean, default=False, nullable=False)
    recipe_scraped = Column(Boolean, default=False, nullable=False)

    def __init__(self, url: str):
        self.url = url

    def __repr__(self):
        return "<{} {} {} {}>".format(
            self.__class__.__name__,
            self.url,
            self.ingredient_scraped,
            self.recipe_scraped,
        )

    def save(self) -> Sitemap:
        exists = (
            session.query(Sitemap).filter_by(url=self.url).first() is not None
        )
        if exists:
            raise FoodScrapeError("URL already exists in table")

        session.add(self)
        session.commit()

        return self

    def scrape_ingredient(self) -> Sitemap:
        self.ingredient_scraped = True
        db.session.add(self)
        db.session.commit()
        return self

    def scrape_recipe(self) -> Sitemap:
        self.recipe_scraped = True
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_ingredient_scraped(limit: int) -> List[Sitemap]:
        sitemaps: List[Sitemap] = (
            db.session.query(Sitemap)
            .filter_by(ingredient_scraped=False)
            .limit(limit)
            .all()
        )
        return sitemaps

    @staticmethod
    def get_recipe_scraped(limit: int) -> List[Sitemap]:
        sitemaps: List[Sitemap] = (
            db.session.query(Sitemap)
            .filter_by(recipe_scraped=False)
            .limit(limit)
            .all()
        )
        return sitemaps


"""
    ------------Ingredient Tables------------
"""


class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    times_seen = Column(Integer, default=1, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return "<{} {} {}>".format(
            self.__class__.__name__, self.name, self.times_seen
        )

    def save(self) -> Ingredient:

        ingredient: Ingredient = (
            session.query(Ingredient).filter_by(name=self.name).first()
        )

        if ingredient is None:
            session.add(self)
            session.commit()
            return self

        ingredient.times_seen += 1
        db.session.commit()

        return ingredient

    @staticmethod
    def get_seen_greater_than_or_eq(times_seen: int) -> List[Ingredient]:
        ingredients: List[Ingredient] = (
            session.query(Ingredient)
            .filter(Ingredient.times_seen >= times_seen)
            .all()
        )
        return ingredients

    @staticmethod
    def get_seen_less_than_or_eq(times_seen: int) -> List[Ingredient]:
        ingredients: List[Ingredient] = (
            session.query(Ingredient)
            .filter(Ingredient.times_seen <= times_seen)
            .all()
        )
        return ingredients

    @staticmethod
    def get_all_by_name(names: List[str]) -> List[Ingredient]:
        names = [str.lower(name) for name in names]

        stmt = select(Ingredient).where(func.lower(Ingredient.name).in_(names))
        return session.execute(stmt).scalars().all()

    @staticmethod
    def get_all() -> List[Ingredient]:
        return session.query(Ingredient).all()


"""
    ------------Recipe Tables------------
"""

"""
   Recipe:  Association Tables
"""
recipe_keyword_association = Table(
    "recipe_keyword_association",
    Base.metadata,
    Column(
        "recipe_id",
        ForeignKey("recipe.id"),
        primary_key=True,
    ),
    Column(
        "keyword_id",
        ForeignKey("recipe_keyword.id"),
        primary_key=True,
    ),
)

"""
   Recipe: Helper Tables
"""


class RecipeKeyword(Base):
    __tablename__ = "recipe_keyword"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    recipes = relationship(
        "Recipe",
        secondary=recipe_keyword_association,
        back_populates="keywords",
    )

    def __init__(self, text: str):
        self.text = text

    def __repr__(self) -> str:
        return "<{} {} {}>".format(
            self.__class__.__name__,
            self.text,
            [recipe.name for recipe in self.recipes],
        )

    @staticmethod
    def get_all() -> List[RecipeKeyword]:
        return session.query(RecipeKeyword).all()


class RecipeInstruction(Base):
    __tablename__ = "recipe_instruction"

    id = Column(Integer, primary_key=True)

    seq_num = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))

    def __init__(self, seq_num: int, text: str):
        self.seq_num = seq_num
        self.text = text

    def __repr__(self) -> str:
        return "<{} {} {}>".format(
            self.__class__.__name__, self.seq_num, self.text
        )

    @staticmethod
    def get_all() -> List[RecipeInstruction]:
        return session.query(RecipeInstruction).all()


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    id = Column(Integer, primary_key=True)

    quantity = Column(String)
    ingredient_name = Column(String)
    original_text = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"))

    def __init__(
        self, quantity: str, ingredient_name: str, original_text: str
    ):
        self.quantity = quantity
        self.ingredient_name = ingredient_name
        self.original_text = original_text

    def __repr__(self) -> str:
        return "<{} {} {}>".format(
            self.__class__.__name__, self.quantity, self.ingredient_name
        )

    @staticmethod
    def get_all() -> List[RecipeIngredient]:
        return session.query(RecipeIngredient).all()


"""
   Recipe: Main
"""


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_published = Column(String)
    description = Column(String)
    image = Column(String)
    author = Column(String)
    recipe_category = Column(String)
    recipe_yield = Column(String)
    cook_time = Column(String)
    prep_time = Column(String)
    total_time = Column(String)
    rating = Column(String)

    instructions = relationship(
        "RecipeInstruction", lazy=True, cascade="all, delete"
    )
    keywords = relationship(
        "RecipeKeyword",
        secondary=recipe_keyword_association,
        back_populates="recipes",
        lazy=True,
    )

    ingredients = relationship(
        "RecipeIngredient", lazy=True, cascade="all, delete"
    )

    def __init__(
        self,
        name: str,
        keywords: List[RecipeKeyword] = [],
        instructions: List[RecipeInstruction] = [],
        ingredients: List[RecipeIngredient] = [],
    ):
        self.name = name
        self.keywords = keywords
        self.instructions = instructions
        self.ingredients = ingredients

    def __repr__(self) -> str:
        return "<{} {} >".format(self.__class__.__name__, self.name)

    def save(self) -> Recipe:
        session.add(self)
        session.commit()
        return self

    @staticmethod
    def get_all() -> List[Recipe]:
        return session.query(Recipe).all()
