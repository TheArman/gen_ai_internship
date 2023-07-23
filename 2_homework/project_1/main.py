import valid_types


class Person:
    age = valid_types.Integer()
    height = valid_types.Float()
    tags = valid_types.List()
    favorite_foods = valid_types.List()
    name = valid_types.String()

