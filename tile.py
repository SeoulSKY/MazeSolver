from pygame import draw, Surface, Rect


class Tile:

    _WHITE = (255, 255, 255)
    _BLACK = (0, 0, 0)
    _GREEN = (0, 255, 0)
    _RED = (255, 0, 0)
    _GREY = (105, 105, 105)

    def __init__(self, display: Surface, rect: Rect):
        """
        Tile constructor
        :param display: The display to display this tile
        :type display: pygame.Surface
        :param rect: The rectangle object for this tile
        :type rect: pygame.Rect
        """
        self._display: Surface = display
        self._rect: Rect = rect
        self._path: bool = False
        self._visited: bool = False
        self._valid: bool = False  # assume the tile is invalid initially
        self._start: bool = False
        self._goal: bool = False

    def set_path(self, value: bool) -> None:
        """
        Set whether the tile is a path or not
        :param value: the value to set
        """
        self._path = value

        if self.is_path():
            self.validate()
        else:
            self.invalidate()

        self.un_visit()

    def set_as_start(self) -> None:
        """
        Set the tile as the start tile
        """
        self._start = True
        self.validate()

    def set_as_goal(self) -> None:
        """
        Set the tile as the goal
        """
        self._goal = True
        self.validate()

    def visit(self) -> None:
        """
        Visit the tile
        """
        self._visited = True

    def un_visit(self) -> None:
        """
        Un-visit the tile
        """
        self._visited = False

    def validate(self) -> None:
        """
        Validate the tile
        """
        self._valid = True

    def invalidate(self) -> None:
        """
        Invalidate the tile
        """
        self._valid = False

    def is_path(self) -> bool:
        """
        Check if the tile is path
        :return: True if the tile is path, False if the tile is wall
        """
        return self._path

    def is_visited(self) -> bool:
        """
        Check if the tile is visited
        :return: True if the tile is visited, False otherwise
        """
        return self._visited

    def is_valid(self) -> bool:
        """
        Check if the tile is valid
        :return: True if the tile is valid, False otherwise
        """
        return self._valid

    def is_start(self) -> bool:
        """
        Check if the tile is the start tile
        :return: True if the tile is the start tile, False otherwise
        """
        return self._start

    def is_goal(self) -> bool:
        """
        Check if the tile is the goal tile
        :return: True if the tile is the goal tile, False otherwise
        """
        return self._goal

    def draw(self) -> None:
        """
        Draw the current state of the tile
        :return:
        """
        if self.is_start() or self.is_goal():
            color = self._RED
        elif not self.is_path():
            color = self._BLACK
        elif self.is_visited():
            if self.is_valid():
                color = self._GREEN
            else:
                color = self._GREY
        else:
            color = self._WHITE

        draw.rect(self._display, color, self._rect)

    def reset(self) -> None:
        """
        Reset the tile to the initial state
        """
        self._path = False
        self._visited = False

        if not self.is_start() and not self.is_goal():
            self._valid = False
