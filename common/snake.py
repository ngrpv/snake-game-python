from prompt_toolkit.data_structures import Point


class Snake:
    def __init__(self, head: Point, tail: Point):
        self.tail = tail
        self.head = head
        self.points = []
        if head.x == tail.x:
            for i in range(min(head.y, tail.y), max(head.y, tail.y)):
                self.points.append(Point(head.x, i))
            self.points.append(Point(head.x, max(head.y, tail.y)))
        elif head.y == tail.y:
            for i in range(min(head.x, tail.x), max(head.x, tail.x)):
                self.points.append(Point(i, head.y))
            self.points.append(Point(max(head.x, tail.x), head.y))
        else:
            raise AttributeError(
                'Head x or y should be equal to tail x or y')

        if self.points[0] != head:
            self.points.reverse()

    def move_down(self):
        self._move(0, 1)

    def move_up(self):
        self._move(0, -1)

    def move_left(self):
        self._move(-1, 0)

    def move_right(self):
        self._move(1, 0)

    def _move(self, dx, dy):
        target_point = Point(self.head.x + dx, self.head.y + dy)
        for i in range(len(self.points)):
            (self.points[i], target_point) = (target_point, self.points[i])


    def get_points(self):
        return self.points
