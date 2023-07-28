from points import Point2D, Point3D


def tester():
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

    a = Point3D(2, 4)           # will error
    b = Point2D(1, 2, 4)        # will error


if __name__ == "__main__":
    tester()
