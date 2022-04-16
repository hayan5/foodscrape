# import datetime as dt

from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields

from foodscrape.database import db
from foodscrape.recipe.models import Recipe

# from .models import
from .serializers import IngredientSchema, recipe_schema, recipe_schemas
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
