"""Slot modul"""


def check_methods(dct: dict) -> None:
    """
        This function checks that the class has attributes __slots__, dimension
    """
    if "__slots__" not in dct:
        raise ValueError("Class must have __slots__ attribute...")

    if "dimension" not in dct:
        raise ValueError("Class must have dimension class attribute...")


class Slot(type):
    """
        A metaclass that assigns additional methods to objects of its type classes
    """

    def __new__(cls, name, bases, class_dct):
        check_methods(class_dct)

        new = super().__new__(cls, name, bases, class_dct)
        new.__hash__ = lambda self: cls.__hash__(new, self)
        new.__eq__ = lambda self, other: cls.__eq__(new, self, other)
        new.__repr__ = lambda self: cls.__repr__(new, self)
        new.__init__ = lambda self, *args: cls.init_(new, self, *args)
        return new

    def __hash__(cls, self):
        values = tuple(getattr(self, attr) for attr in cls.__slots__)
        return hash(values)

    def __eq__(cls, self, other):
        if isinstance(other, cls):
            return all(getattr(self, attr) == getattr(other, attr) for attr in cls.__slots__)

        return False

    def __repr__(cls, self):
        coordinates = ', '.join(str(getattr(self, slot)) for slot in cls.__slots__)
        return f"Class name: {cls.__name__}, cords: {coordinates}"

    def init_(cls, self, *args):
        if len(args) != cls.dimension:
            raise ValueError(f"Dimension must be equal count of args...")

        for i, value in enumerate(args):
            setattr(self, cls.__slots__[i], value)
