from common.enums import Direction
from common.point import Point


class Snake:
    """Snake entity for classic snake game"""
    def __init__(self, head: Point, tail: Point):
        self.tail = tail
        self.head = head
        self.points = []
        self.previous_tail_position = tail
        self._coordinate_limits = None

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

    def move(self, direction: Direction) -> None:
        """Move the snake one block in the given direction"""
        self.teleport(self.head + direction.value)

    def teleport(self, position: Point):
        """Make the snake by teleporting its head to given position"""
        if self._coordinate_limits:
            position %= self._coordinate_limits

        if position == self.points[1]:
            raise AttributeError("Snake can't move on opposite direction")
        self.previous_tail_position = self.points[-1]
        for i in range(len(self.points)):
            self.points[i], position = position, self.points[i]
        self.head = self.points[0]
        self.tail = self.points[-1]

    def grow(self):
        """Grows snake to one block in tail"""
        self.points.append(self.previous_tail_position)

    def set_coordinate_limits(self, x, y):
        """Coordinates limit for snake. If snake out of bounds it'll appear from other side of map"""
        self._coordinate_limits = Point(x, y)

    def get_points(self):
        return self.points

    def can_collide_with_itself(self, direction: Direction) -> bool:
        """Checks if snake can collide with self on moving given direction"""
        target = self.head + direction.value
        if target in self.points[:-1]:
            return True
        return False
