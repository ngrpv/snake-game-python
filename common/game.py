from random import randint

from common.enums import Direction, MapCellType, PortalDestination
from common.level import GameLevel
from common.point import Point
from common.game_map import Portal


class Game:
    def __init__(self, levels: list[GameLevel]):
        self._next_level_portal = None
        self._levels = levels
        self._level = None
        self._level_number = 0
        self._is_game_clear = False
        self._food_point = None
        self._previous_direction = None
        self._score = 0
        self._score_on_level = 0
        self._snake = None
        self._is_game_over = not self._next_level()

    def _next_level(self) -> bool:
        self._score_on_level = 0
        if len(self._levels) == 0:
            self._is_game_clear = True
            return False

        level = self._levels.pop(0)
        self._level_number += 1
        self._level = level
        if not self._snake:
            self._snake = level.snake
        else:
            self._snake.teleport(level.snake.head)
            self._snake.decrease_to_one()
        if not self._previous_direction:
            self._previous_direction = level.start_direction
        self._map = level.map
        self._snake.set_coordinate_limits(
            self._map.width,
            self._map.height)
        self._next_level_portal = None
        self._next_food()
        return True

    def _get_random_empty_point(self, direction_free: Direction = None) -> Point:
        """Returns random point, which is empty on current map. If direction_free is provided, there
        will be an additional requirement for random point to have empty neighbour at provided location"""
        is_point_generated = False
        candidate = None
        while not is_point_generated:
            x = randint(0, self._map.width - 1)
            y = randint(0, self._map.height - 1)
            candidate = Point(x, y)
            if self.get(x, y) == MapCellType.Empty:
                if direction_free:
                    additional_point = candidate + direction_free.value
                    if self.get(additional_point.x, additional_point.y) != MapCellType.Empty:
                        continue
                is_point_generated = True
        return candidate

    def _next_food(self) -> None:
        self._food_point = self._get_random_empty_point()

    @property
    def map_dimensions(self) -> Point:
        return Point(self._map.width, self._map.height)

    @property
    def _map_size(self):
        return Point(self._map.width, self._map.height)

    @property
    def score(self):
        return self._score

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @property
    def level_number(self) -> int:
        return self._level_number

    @property
    def is_game_clear(self) -> bool:
        return self._is_game_clear

    def get(self, x: int, y: int) -> MapCellType:
        """Get current map representation for view"""
        point = Point(x, y)

        if self._next_level_portal and point == self._next_level_portal.position:
            return MapCellType.PortalIn

        if point == self._food_point:
            return MapCellType.Food
        for candidate in self._snake.get_points():
            candidate_truncated = candidate % self._map_size
            if candidate_truncated == point:
                return MapCellType.Snake

        return self._map.get(x, y)

    def is_direction_valid(self, direction: Direction) -> bool:
        """Check, if submitted direction is valid to move"""
        return (not self._previous_direction or
                self._previous_direction.value != -direction.value)

    def _process_portal(self, portal: Portal) -> None:
        if portal.destination_type == PortalDestination.StaticPoint:
            self._snake.teleport(portal.destination)
            return
        if portal.destination_type == PortalDestination.RandomPoint:
            destination = self._get_random_empty_point()
            self._snake.teleport(destination)
            return
        if portal.destination_type == PortalDestination.NextLevel:
            self._is_game_over = not self._next_level()
            return

        raise ValueError(f"Unknown portal destination type at coordinates {portal.position}")

    def move(self, direction: Direction = None) -> None:
        """Move snake in specified direction"""
        if not direction:
            direction = self._previous_direction

        if not self.is_direction_valid(direction):
            raise AttributeError("Snake can't move on opposite direction")

        if self._is_game_over:
            return

        self._previous_direction = direction
        head = self._snake.head % self._map_size
        if (self._snake.can_collide_with_itself(direction) or
                self._map.get(head.x, head.y) == MapCellType.Obstacle):
            self._is_game_over = True
            return

        portals = (self._next_level_portal,) + self._map.portals
        portals_starts = {x.position if x else None for x in portals}
        if head in portals_starts:
            for portal in portals:
                if not portal:
                    continue
                if portal.position == head:
                    self._process_portal(portal)
                    break
        else:
            self._snake.move(direction)

        if self._snake.head == self._food_point:
            self._snake.grow()
            self._score += 1
            self._score_on_level += 1
            if self._score_on_level >= self._level.clear_score and \
                    self._next_level_portal is None:
                position = self._get_random_empty_point()
                self._next_level_portal = Portal(position, PortalDestination.NextLevel)
            self._next_food()
