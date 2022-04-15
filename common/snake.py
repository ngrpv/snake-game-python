from common.enums import Direction
from common.Point import Point


class Snake:
    '''Snake entity for classic snake game'''
    def __init__(self, head: Point, tail: Point):
        if head.x < 0 or head.y < 0 or tail.x < 0 or tail.y < 0:
            raise AttributeError('Initial coordinates must be non-negative')
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
        '''Move the snake one block in the given direction'''
        target_point = Point(
            self.head.x + direction.value.x,
            self.head.y + direction.value.y)
        if self._coordinate_limits:
            limits = self._coordinate_limits
            target_point = Point(
                (limits.x + target_point.x) % limits.x,
                (limits.y + target_point.y) % limits.y)

        if len(self.points) > 1 and target_point == self.points[1]:
            raise AttributeError("Snake can't move on opposite direction")
        self.previous_tail_position = self.points[-1]
        for i in range(len(self.points)):
            self.points[i], target_point = target_point, self.points[i]
        self.head = self.points[0]
        self.tail = self.points[-1]

    def grow(self):
        '''Grow snake to one block in tail'''
        self.points.append(self.previous_tail_position)

    def set_coordinate_limits(self, x, y):
        '''Coordinates limit for snake. If snake out of bounds it'll appear from other side of map'''
        if x < 1 or y < 1:
            raise AttributeError('limits should be more than zero')
        self._coordinate_limits = Point(x, y)

    def get_points(self):
        '''Returns points of snake'''
        return self.points

    def can_collide_with_itself(self, direction: Direction) -> bool:
        '''Checks if snake can collide with self on moving given direction'''
        target = Point(self.head.x + direction.value.x,
                       self.head.y + direction.value.y)
        if target in self.points[:-1]:
            return True
        return False
