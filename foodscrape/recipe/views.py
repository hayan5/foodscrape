# import datetime as dt

from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields
from sqlalchemy import any_, func, or_, select

from foodscrape.database import db

# from foodscrape.ingredient.models import RawIngredient
from foodscrape.ingredient.serializers import raw_ingredient_schemas
from foodscrape.recipe.models import Ingredient, Recipe

# from .models import
from .serializers import (
    IngredientSchema,
    recipe_schema,
    recipe_schemas,
    search_schema,
)
from .service import get_data

blueprint = Blueprint("recipe", __name__)


@blueprint.route("/api/recipe", methods=("POST",))
@use_kwargs({"url": fields.Str()})
@marshal_with(recipe_schema)
def recipe(url):

    return get_data(url)


ingredient_schemas = IngredientSchema(many=True)


@blueprint.route("/api/recipe", methods=("GET",))
@marshal_with(recipe_schemas)
def get_sitemap():
    sitemaps = db.session.query(Recipe).all()

    return sitemaps


# @blueprint.route("/api/recipe/find", methods=("GET",))
# @use_kwargs(search_schema)
# @marshal_with(raw_ingredient_schemas)
# def find_recipes(ingredient_name):
#     # print(ingredient_name)
#     # stmt = select(RawIngredient).where(RawIngredient.name.in_(ingredient_name))
#     raw_ids = select(RawIngredient.id).where(
#         or_(
#             *[RawIngredient.name.like(f"%{name}%") for name in ingredient_name]
#         )
#     )

#     stmt = select(Recipe.ingredients).count()
#     stmt = select(func.count("*")).select_from("ingredient")
#     print(stmt)
#     # db.session.query()

#     return a
