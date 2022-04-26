from __future__ import annotations

from typing import List, Union

from foodscrape.database import Column, Model
from foodscrape.extensions import db
from foodscrape.logger import get_logger

logger = get_logger(__name__)


class Sitemap(Model):
    __tablename__ = "sitemap"

    id = Column(db.Integer, primary_key=True)
    url = Column(db.String, unique=True, nullable=False)

    ingredient_scraped = Column(db.Boolean, default=False, nullable=False)
    recipe_scraped = Column(db.Boolean, default=False, nullable=False)

    def __init__(self, url: str):
        self.url = url

    def __repr__(self):
        return "<{} {} {} {}>".format(
            self.__class__.__name__,
            self.url,
            self.ingredient_scraped,
            self.recipe_scraped,
        )

    def save(self) -> Union[Sitemap, None]:
        exists = (
            db.session.query(Sitemap).filter_by(url=self.url).first()
            is not None
        )
        if not exists:
            db.session.add(self)
            db.session.commit()
            return self

        return None

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


# class Ingredient(Model):
#     __tablename__ = "ingredient"

#     id = Column(db.Integer, primary_key=True)
#     name = Column(db.String, unique=True, nullable=False)
#     times_seen = Column(db.Integer, default=1, nullable=False)


# class Recipe(Model):  # type: ignore
#     __tablename__ = "recipe"

#     id = Column(db.Integer, primary_key=True)
#     name = Column(db.String)
#     date_published = Column(db.String)
#     description = Column(db.String)
#     image = Column(db.String)
#     author = Column(db.String)
#     recipe_category = Column(db.String)
#     recipe_yield = Column(db.String)
#     cook_time = Column(db.String)
#     prep_time = Column(db.String)
#     total_time = Column(db.String)
#     rating = Column(db.String)

# keywords = db.relationship(
#     "Keyword", secondary=recipe_keyword, back_populates="recipes"
# )

# instructions = db.relationship("Instruction", backref="recipe", lazy=True)
# ingredients = db.relationship(
#     "RecipeIngredient", backref="recipe", lazy=True
# )


# class Keyword(Model):
#     __tablename__ = "keyword"

#     id = Column(db.Integer, primary_key=True)
# text = db.Column(db.String)
# recipes = db.relationship(
#     "Recipe", secondary=recipe_keyword, back_populates="keywords"
# )


# class Instruction(Model):
#     __tablename__ = "instruction"

#     id = db.Column(db.Integer, primary_key=True)
# seq_num = db.Column(db.Integer)
# text = db.Column(db.String)
# recipe_id = db.Column(
#     db.Integer, db.ForeignKey("recipe.id"), nullable=False
# )


# class Recipe_Ingredient(Model):
#     __tablename__ = "recipe_ingredient"

#     id = db.Column(db.Integer, primary_key=True)
# text = db.Column(db.String)
# quantity = db.Column(db.String)
# ingredient_name = db.Column(db.String)
# recipe_id = db.Column(
#     db.Integer, db.ForeignKey("recipe.id"), nullable=False
# )


# recipe_keyword = db.Table(
#     "recipe_keyword",
#     db.Column("id", db.Integer, primary_key=True),
#     db.Column(
#         "keyword_id",
#         db.Integer,
#         db.ForeignKey("keyword.id", ondelete="CASCADE"),
#         nullable=False,
#     ),
#     db.Column(
#         "recipe_id",
#         db.Integer,
#         db.ForeignKey("recipe.id", ondelete="CASCADE"),
#         nullable=False,
#     ),
# )
