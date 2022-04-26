from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields

from foodscrape.database import db
from foodscrape.sitemap.models import Sitemap

from .models import Ingredient
from .serializers import raw_ingredient_schemas
from .service import find_ingredients_from_url

blueprint = Blueprint("ingredient", __name__)


@blueprint.route("/api/ingredient", methods=("POST",))
@use_kwargs({"amount": fields.Int()})
@marshal_with(raw_ingredient_schemas)
def scrape(amount: int):
    sitemaps = (
        Sitemap.query.filter(Sitemap.is_ingredients_scraped == False)
        .limit(amount)
        .all()
    )
    all_ingredients = []
    for sitemap in sitemaps:
        sitemap.is_ingredients_scraped = True

        ingredients = find_ingredients_from_url(sitemap.url)
        for i in ingredients:
            all_ingredients.append(i)
    db.session.commit()
    return all_ingredients
