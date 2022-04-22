from marshmallow import Schema, fields


class RawIngredientSchema(Schema):

    name = fields.String()
    times_seen = fields.Integer()


raw_ingredient_schema = RawIngredientSchema()
raw_ingredient_schemas = RawIngredientSchema(many=True)
