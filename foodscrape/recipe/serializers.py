from marshmallow import Schema, fields


class KeywordSchema(Schema):
    text = fields.String()


class InstructionSchema(Schema):
    __tablename__ = "instruction"

    seq_num = fields.Integer()
    text = fields.Str()
    recipe_id = fields.Integer()


class IngredientSchema(Schema):
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
    ingredients = fields.List(fields.Nested(IngredientSchema))
    keywords = fields.List(fields.Nested(KeywordSchema))


class SearchSchema(Schema):
    ingredient_name = fields.Str()


recipe_schema = RecipeSchema()
recipe_schemas = RecipeSchema(many=True)
keyword_schema = KeywordSchema()
keyword_schemas = KeywordSchema(many=True)
ingredient_schema = IngredientSchema()
ingredient_schemas = IngredientSchema(many=True)
instruction_schema = InstructionSchema()
instruction_schemas = InstructionSchema(many=True)
search_schema = SearchSchema(many=True)
