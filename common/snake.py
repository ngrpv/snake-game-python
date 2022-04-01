from prompt_toolkit.data_structures import Point


class Snake:
    def __init__(self, head: Point, tail: Point):
        self.tail = tail
        self.head = head
        self.points = [tail]
        if head.x == tail.x:
            for i in range(head.y, tail.y):
                self.points.append(Point(head.x, i))
        elif head.y == tail.y:
            for i in range(head.x, tail.x):
                self.points.append(Point(i, head.y))
        else:
            raise AttributeError(
                'Head x or y should be equal to tail x or y')

    def move_down(self):
        self._move(0, 1)

    def move_up(self):
        self._move(0, -1)

    def move_left(self):
        self._move(-1, 0)

    def move_right(self):
        self._move(1, 1)

    def _move(self, dx, dy):
        previous = Point(self.head.x + dx, self.head.y + dy)
        for i in range(len(self.points)):
            (self.points[i], previous) = (previous, self.points[i])


    def get_points(self):
        return self.points
