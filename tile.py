import pygame.draw


class Tile:

    _WHITE = (255, 255, 255)
    _BLACK = (0, 0, 0)
    _GREEN = (0, 255, 0)
    _RED = (255, 0, 0)

    def __init__(self, display, rect):
        """
        Tile constructor
        :param display: The display to display this tile
        :type display: pygame.Surface
        :param rect: The rectangle object for this tile
        :type rect: pygame.Rect
        """
        self._display = display
        self._rect = rect
        self._path = False
        self._visited = False
        self._valid = False  # assume the tile is invalid initially
        self._start = False
        self._goal = False

    def set_path(self, value):
        """
        Set whether the tile is a path or not
        :param value: the value to set
        :type value: bool
        """
        self._path = value

        if self.is_path():
            self._valid = True
        else:
            self.invalidate()

    def set_as_start(self):
        self._valid = True
        self._start = True

    def set_as_goal(self):
        self._valid = True
        self._goal = True

    def visit(self):
        self._visited = True

    def invalidate(self):
        self._valid = False

    def is_path(self):
        return self._path

    def is_visited(self):
        return self._visited

    def is_valid(self):
        return self._valid

    def is_start(self):
        return self._start

    def is_goal(self):
        return self._goal

    def draw(self):
        """
        Draw the current state of the tile
        :return:
        """
        if self.is_start() or self.is_goal():
            color = self._RED
        elif not self.is_path():
            color = self._BLACK
        elif self.is_visited() and self.is_valid():
            color = self._GREEN
        else:
            color = self._WHITE

        pygame.draw.rect(self._display, color, self._rect)

    def reset(self):
        self._path = False
        self._visited = False

        if not self.is_start() and not self.is_goal():
            self._valid = False
