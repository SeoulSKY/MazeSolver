import math

from pygame import Surface, Rect
from tile import Tile


class Maze:
    def __init__(self, display, num_tiles):
        """
        Maze constructor
        :param display: pygame display
        :type display: Surface
        :param num_tiles: (x, y)
        :type num_tiles: Tuple[int, int]
        """
        self._display = display
        self._x_num_tiles = num_tiles[0]
        self._y_num_tiles = num_tiles[1]
        self._board = []   # 2d list for tiles
        self._cursor = [0, 0]   # cursor of the board to point a certain tile

        self._tile_width = display.get_width() / self._x_num_tiles
        self._tile_height = display.get_height() / self._y_num_tiles

        for i in range(self._x_num_tiles):
            row = []    # current row for the board

            for j in range(self._y_num_tiles):
                rect = Rect(self._tile_width * i, self._tile_height * j, self._tile_width, self._tile_height)
                tile = Tile(display, rect)
                row.append(tile)

            self._board.append(row)

        # make the tile that is pointed by the cursor as start
        start_tile = self._board[self._cursor[0]][self._cursor[1]]
        start_tile.set_as_start()

        # make the bottom right tile as the goal
        goal_tile = self._board[self._x_num_tiles - 1][self._y_num_tiles - 1]
        goal_tile.set_as_goal()

    def draw(self):
        """
        Draw the maze object
        """
        for i in range(self._x_num_tiles):
            for j in range(self._y_num_tiles):
                self._board[i][j].draw()

    def click(self, pos):
        """
        Click the tile in the given position
        :param pos: the position to click
        :type pos: Tuple[int, int]
        """
        target_tile = self._board[math.floor(pos[0] / self._tile_width)][math.floor(pos[1] / self._tile_height)]

        if not target_tile.is_start() and not target_tile.is_goal():
            target_tile.set_as_wall()

    def solve(self):
        start_tile = self._board[self._cursor[0]][self._cursor[1]]
        self._solve(start_tile) # call the helper method

    def _solve(self, start):
        """
        Helper method to solve the maze
        :param start: The tile to start solving
        :type start: Tile
        :return: True if the goal has reached, False otherwise
        """
        pass

    def reset(self):
        """
        Reset the board
        """
        for i in range(self._x_num_tiles):
            for j in range(self._y_num_tiles):
                tile = self._board[i][j]
                tile.reset()