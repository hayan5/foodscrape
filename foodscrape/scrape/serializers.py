from marshmallow import Schema, fields


class SitemapSchema(Schema):
    id = fields.Str()
    url = fields.Url()
    ingredient_scraped = fields.Boolean()
    recipe_scraped = fields.Boolean()


class IngredientSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    times_seen = fields.Str()


class KeywordSchema(Schema):
    text = fields.String()


class InstructionSchema(Schema):
    __tablename__ = "instruction"

    seq_num = fields.Integer()
    text = fields.Str()
    recipe_id = fields.Integer()


class RecipeIngredientSchema(Schema):
    quantity = fields.Str()
    ingredient_name = fields.Str()
    text = fields.Str()
    recipe_id = fields.Integer()


class RecipeSchema(Schema):  # type: ignore

    id = fields.Integer()
    name = fields.Str()
    date_published = fields.Str()
    description = fields.Str()
    image = fields.Str()
    author = fields.Str()
    recipe_category = fields.Str()
    recipe_yield = fields.Str()
    cook_time = fields.Str()
    prep_time = fields.Str()
    total_time = fields.Str()
    rating = fields.Str()

    instructions = fields.List(fields.Nested(InstructionSchema))
    ingredients = fields.List(fields.Nested(RecipeIngredientSchema))
    keywords = fields.List(fields.Nested(KeywordSchema))


sitemap_schema = SitemapSchema()
sitemap_schemas = SitemapSchema(many=True)
ingredient_schemas = IngredientSchema(many=True)
recipe_schemas = RecipeSchema(many=True)
