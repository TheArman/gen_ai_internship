"""Points modul"""

from slot import Slot


class Point2D(metaclass=Slot):
    """
        This class describes points in 2D area:
        takes two arguments,
        which are the coordinates of a point in 2D area
    """

    __slots__ = ('_x', '_y')
    dimension = 2

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Point3D(metaclass=Slot):
    """
            This class describes points in 3D area:
            takes three arguments,
            which are the coordinates of a point in 3D area
    """

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


class Point4D(metaclass=Slot):
    """
            This class describes points in 4D area:
            takes four arguments,
            which are the coordinates of a point in 4D area
    """

    __slots__ = ('_x', '_y', '_z', '_k')
    dimension = 4

    @property
    def x(self):
        return self._x

    def y(self):
        return self._y

    def z(self):
        return self._z

    def k(self):
        return self._k


class Point5D(metaclass=Slot):
    """
            This class describes points in 5D area:
            takes five arguments,
            which are the coordinates of a point in 5D area
    """

    __slots__ = ('_x', '_y', '_z', '_k', '_m')
    dimension = 5

    @property
    def x(self):
        return self._x

    def y(self):
        return self._y

    def z(self):
        return self._z

    def k(self):
        return self._k

    def m(self):
        return self._m
