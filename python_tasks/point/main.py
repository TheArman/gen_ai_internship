"""Main modul"""

from points import Point2D, Point3D, Point4D, Point5D


def tester():
    """
        This function performs checks on Point2D, Point3D, Point4D, Point5D classes
    """

    point1 = Point2D(1, 2)
    point2 = Point2D(2, 3)
    print(point1 == point2)
    print(hash(point1))
    print(point1)

    point3 = Point3D(1, 2, 3)
    point4 = Point3D(4, 5, 6)
    print(point3 == point4)
    print(hash(point2))
    print(point3)

    point5 = Point4D(1, 3, 4, 2)
    point6 = Point4D(1, 3, 4, 2)
    point7 = Point5D(3, 2, 1, 4, 5)
    point8 = Point5D(1, 2, 3, 4, 5)
    print(point5 == point6)
    print(point7 == point8)
    print(hash(point5))
    print(hash(point7))
    print(point6)
    print(point8)

    # a = Point3D(2, 4)           # will error
    # b = Point2D(1, 2, 4)        # will error
    # c = Point5D(1, 4, 5)        # will error
    # d = Point4D(3, 2, 1, 5, 6)  # will error


if __name__ == "__main__":
    tester()
