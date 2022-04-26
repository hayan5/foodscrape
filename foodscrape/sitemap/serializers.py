from marshmallow import Schema, fields


class SitemapSchema(Schema):
    id = fields.Str()
    url = fields.Url()
    is_recipe_scraped = fields.Boolean()
    is_ingredients_scraped = fields.Boolean()
    scraped_date = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


sitemap_schema = SitemapSchema()
sitemap_schemas = SitemapSchema(many=True)
