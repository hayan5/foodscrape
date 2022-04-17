from marshmallow import Schema, fields


class RawIngredientSchema(Schema):

    name = fields.String()


raw_ingredient_schema = RawIngredientSchema()
raw_ingredient_schemas = RawIngredientSchema(many=True)
