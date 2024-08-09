class Int:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.min_value is not None and self.min_value > value:
            raise ValueError(f'Value must be greater or equal to {self.min_value}')

        if self.max_value is not None and self.max_value < value:
            raise ValueError(f'Value must be less or equal to {self.max_value}')

        if not isinstance(value, int):
            raise ValueError('Value must be int.')

        instance.__dict__[self.name] = value


class Point2D:
    x = Int(min_value=0)
    y = Int(min_value=0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Point in 2D area'

    def __repr__(self):
        return f'Point({self.x}, {self.y})'


class Point2DSequence:
    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f'{self.name} must have at least {self.min_length} elements.')

        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f'{self.name} cannot have more than {self.max_length} elements.')

        if isinstance(value, (list, tuple)):
            for item in value:
                if not isinstance(item, Point2D):
                    raise ValueError('Each element must be Point2D type.')
        else:
            raise ValueError('Value must be type list or tuple.')

        instance.__dict__[self.name] = value


class Polygon:
    vertices = Point2DSequence(2, 7)

    def __init__(self, *vertices):
        self.vertices = list(vertices)

    def append(self, point):
        if isinstance(point, Point2D):
            self.vertices.append(point)
        else:
            raise Exception(f'Argument must type Point2D and max length must be {self.vertices.max_length}')

    def __repr__(self):
        return f'{self.__class__.__name__}'
