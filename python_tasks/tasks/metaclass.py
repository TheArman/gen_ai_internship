class TypeChecking(type):

    def __new__(cls, name, bases, dct):
        new = super().__new__(cls, name, bases, dct)
        for i, j in new.__dict__.items():
            if not i.startswith("__"):
                if type(new.__dict__[i]) != new.__annotations__[i]:
                    raise Exception("Incorrect type")
        return new


class Triangle(metaclass=TypeChecking):
    a: int = 'a'  # incorrect
    b: int = 92  # correct
    c: float = 2.5  # correct


class Spam(metaclass=TypeChecking):
    x: int = 12  # correct
    y: str = 'spam'  # correct
