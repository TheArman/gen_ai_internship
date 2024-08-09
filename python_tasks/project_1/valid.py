class ValidType:
    def __init__(self, tmp_type):
        self.tmp_type = tmp_type

    def __set_name__(self, instance, property_name):
        self.property_name = property_name

    def __set__(self, instance, value):
        if not isinstance(value, self.tmp_type):
            raise ValueError("Your value is invalid")

        instance.__dict__[self.property_name] = value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.property_name, None)
