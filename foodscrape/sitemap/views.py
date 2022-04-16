# import datetime as dt

from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields

from foodscrape.database import db

from .models import Sitemap
from .serializers import sitemap_schemas
from .service import scrape_sitemap

blueprint = Blueprint("sitemap", __name__)


@blueprint.route("/api/sitemap", methods=("POST",))
@use_kwargs({"url": fields.Str()})
def sitemap(url):
    scrape_sitemap(url)
    return jsonify(message=url)


@blueprint.route("/api/sitemap", methods=("GET",))
@marshal_with(sitemap_schemas)
def get_sitemap():
    sitemaps = db.session.query(Sitemap).all()

    return sitemaps
