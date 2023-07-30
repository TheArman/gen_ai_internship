class SingletonMeta(type):
    __instance = None

    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            print(f'Instance created: {id(cls.__instance)}')
            cls.__instance = cls
        return cls.__instance


class Database(metaclass=SingletonMeta):

    def select_query(self):
        print('Query selected')

    def add_column(self):
        print("Column added")


def tester():
    db0 = Database()
    db1 = Database()
    db2 = Database()
    db3 = Database()

    print(db1 is db3)
    print(db3 is db1)
    print(db1 is db0)
    print(db2 is db3)


if __name__ == "__main__":
    tester()
