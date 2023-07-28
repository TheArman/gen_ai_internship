from slot import Slot


class Point2D(metaclass=Slot):
    __slots__ = ('_x', '_y')
    dimension = 2

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Point3D(metaclass=Slot):
    __slots__ = ('_x', '_y', '_z')
    dimension = 3

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z
