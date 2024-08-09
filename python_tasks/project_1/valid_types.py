import valid


class Integer(valid.ValidType):
    def __init__(self):
        super().__init__(int)


class Float(valid.ValidType):
    def __init__(self):
        super().__init__(float)


class List(valid.ValidType):
    def __init__(self):
        super().__init__(list)


class String(valid.ValidType):
    def __init__(self):
        super().__init__(str)
