from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields

from .models import Ingredient, Recipe, Sitemap
from .serializers import ingredient_schemas, recipe_schemas, sitemap_schemas
from .service import (
    get_recipes_by_ingredients,
    scrape_ingredients,
    scrape_recipes,
    scrape_sitemap_from_url,
)

blueprint = Blueprint("scrape", __name__)


@blueprint.route("/api/sitemap", methods=("POST",))
@use_kwargs({"url": fields.Str()})
@marshal_with(sitemap_schemas)
def sitemap(url):
    sitemaps = scrape_sitemap_from_url(url)
    return sitemaps


@blueprint.route("/api/sitemap", methods=("GET",))
@marshal_with(sitemap_schemas)
def get_sitemaps():
    sitemaps = Sitemap.get_recipe_scraped(100)
    return sitemaps


@blueprint.route("/api/ingredient", methods=("POST",))
@use_kwargs({"limit": fields.Int()})
@marshal_with(ingredient_schemas)
def make_ingredient(limit):
    return scrape_ingredients(limit)


@blueprint.route("/api/ingredient", methods=("GET",))
@marshal_with(ingredient_schemas)
def get_ingredient():
    return Ingredient.get_all()


@blueprint.route("/api/recipe", methods=("POST",))
@use_kwargs({"limit": fields.Int()})
@marshal_with(recipe_schemas)
def make_recipes(limit):
    return scrape_recipes(limit)


@blueprint.route("/api/recipe", methods=("GET",))
@use_kwargs({"limit": fields.Int()})
@marshal_with(recipe_schemas)
def get_recipes():
    return Recipe.get_all()


@blueprint.route("/api/find", methods=("GET",))
@use_kwargs({"ingredients": fields.List(fields.Str())})
@marshal_with(recipe_schemas)
def get_recipes_ingredients(ingredients):
    return get_recipes_by_ingredients(ingredients)
