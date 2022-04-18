from numbers import Real


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self):
        return "Point(x={},y={})".format(self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Can perform addition Point with Point only")
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if not isinstance(other, Real):
            raise TypeError("Can multiply Point with real numbers only")
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return -1 * self

    def __mod__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Can perform modular division between Points only")
        both = self + other
        return Point(both.x % other.x, both.y % other.y)
