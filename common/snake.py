from common.enums import Direction
from prompt_toolkit.data_structures import Point


class Snake:
    def __init__(self, head: Point, tail: Point):
        self.tail = tail
        self.head = head
        self.points = []
        self.previous_tail_position = tail
        self.is_dead = False
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
        target_point = Point(self.head.x + direction.value.x,
                             self.head.y + direction.value.y)
        if self._can_die_on_moving(target_point):
            self.is_dead = True
            return
        self.previous_tail_position = self.points[-1]
        for i in range(len(self.points)):
            self.points[i], target_point = target_point, self.points[i]
        self.head = self.points[0]
        self.tail = self.points[-1]

    def grow(self):
        self.points.append(self.previous_tail_position)

    def get_points(self):
        return self.points

    def _can_die_on_moving(self, target: Point) -> bool:
        if target in self.points[:-1]:
            return True
        return False
