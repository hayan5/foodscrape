from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields

from foodscrape.database import db

from .models import ScrapedIngredient
from .serializers import raw_ingredient_schemas
from .service import find_ingredients_from_url

blueprint = Blueprint("ingredient", __name__)


@blueprint.route("/api/ingredient", methods=("POST",))
@use_kwargs({"url": fields.Str()})
@marshal_with(raw_ingredient_schemas)
def scrape(url: str):
    ingredients = find_ingredients_from_url(url)
    return ingredients


@blueprint.route("/api/ingredient", methods=("GET",))
@marshal_with(raw_ingredient_schemas)
def get_all():
    res = db.session.query(ScrapedIngredient).all()
    return res
