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
        self._wall = False
        self._visited = False
        self._valid = True  # assume the tile is valid initially
        self._start = False
        self._goal = False

    def set_as_wall(self):
        self._wall = True

    def set_as_start(self):
        self._start = True

    def set_as_goal(self):
        self._goal = True

    def visit(self):
        self._visited = True

    def invalidate(self):
        self._valid = False

    def is_wall(self):
        return self._wall

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
        if self.is_wall():
            color = self._BLACK
        elif self.is_visited() and self.is_valid():
            color = self._GREEN
        elif self.is_start() or self.is_goal():
            color = self._RED
        else:
            color = self._WHITE

        pygame.draw.rect(self._display, color, self._rect)

    def reset(self):
        self._wall = False
        self._visited = False
        self._valid = True
