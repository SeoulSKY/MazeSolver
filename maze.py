import math
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Tuple

import pygame
from pygame import Surface, Rect

from tile import Tile


class Maze:
    def __init__(self, display: Surface, num_tiles: Tuple[int, int]):
        """
        Maze constructor
        :param display: pygame display
        :param num_tiles: (x, y)
        """
        self._executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)

        self._display: Surface = display
        self._x_num_tiles: int = num_tiles[0]
        self._y_num_tiles: int = num_tiles[1]
        self._board = []  # 2d list for tiles
        self._cursor = [0, 0]  # cursor of the board to point a certain tile

        self._tile_width: float = display.get_width() / self._x_num_tiles
        self._tile_height: float = display.get_height() / self._y_num_tiles

        for i in range(self._x_num_tiles):
            row = []  # current row for the board

            for j in range(self._y_num_tiles):
                rect = Rect(self._tile_width * i, self._tile_height * j, self._tile_width, self._tile_height)
                tile = Tile(display, rect)
                row.append(tile)

            self._board.append(row)

        # make the tile that is pointed by the cursor as start
        start_tile = self._get_tile()
        start_tile.set_as_start()

        # make the bottom right tile as the goal
        goal_tile = self._board[self._x_num_tiles - 1][self._y_num_tiles - 1]
        goal_tile.set_as_goal()

    def draw(self) -> None:
        """
        Draw the maze object
        """
        for i in range(self._x_num_tiles):
            for j in range(self._y_num_tiles):
                self._board[i][j].draw()

    def set_as_path(self, pos: Tuple[int, int]) -> None:
        """
        Set the tile on the given position as path
        :param pos: the position
        """
        target_tile = self._board[math.floor(pos[0] / self._tile_width)][math.floor(pos[1] / self._tile_height)]

        if not target_tile.is_start() and not target_tile.is_goal():
            target_tile.set_path(True)

    def set_as_wall(self, pos: Tuple[int, int]) -> None:
        """
        Set the tile on the given position as wall
        :param pos: the position
        """
        target_tile = self._board[math.floor(pos[0] / self._tile_width)][math.floor(pos[1] / self._tile_height)]

        if not target_tile.is_start() and not target_tile.is_goal():
            target_tile.set_path(False)

    def solve(self, show_step: bool) -> Future[bool]:
        """
        Solve the maze
        :return: A future that will return True if the goal has been reached, or False otherwise
        """
        return self._executor.submit(self._solve, show_step)

    def _solve(self, show_step: bool) -> bool:
        """
        Helper to solve the maze
        :return: True if the goal has been reached, False otherwise
        """
        self._get_tile().visit()    # set current tile as visited

        if show_step:
            pygame.time.wait(10)

        # base case
        if self._get_tile().is_goal():
            return True

        found_goal = False

        # visit the lower tile
        if self._has_lower_tile() and not self._get_lower_tile().is_visited() and \
                self._get_lower_tile().is_valid():
            self._move_down()

            found_goal = self._solve(show_step)

            if found_goal:
                return True
            else:
                self._get_tile().invalidate()   # invalidate the downer tile
                self._move_up()  # revert the cursor

        # visit the right tile
        if not found_goal and self._has_right_tile() and not self._get_right_tile().is_visited() and \
                self._get_right_tile().is_valid():
            self._move_right()

            found_goal = self._solve(show_step)

            if found_goal:
                return True
            else:
                self._get_tile().invalidate()   # invalidate the right tile
                self._move_left()  # revert the cursor

        # visit the upper tile
        if not found_goal and self._has_upper_tile() and not self._get_upper_tile().is_visited() and \
                self._get_upper_tile().is_valid():
            self._move_up()

            found_goal = self._solve(show_step)

            if found_goal:
                return True
            else:
                self._get_tile().invalidate()   # invalidate the upper tile
                self._move_down()   # revert the cursor

        # visit the left tile
        if not found_goal and self._has_left_tile() and not self._get_left_tile().is_visited() and \
                self._get_left_tile().is_valid():
            self._move_left()

            found_goal = self._solve(show_step)

            if found_goal:
                return True
            else:
                self._get_tile().invalidate()   # invalidate the left tile
                self._move_right()  # revert the cursor

        return False

    def _has_upper_tile(self) -> bool:
        """
        Check if there is the upper tile from the cursor.
        :return: True if it has, False otherwise
        """
        return self._cursor[1] > 0

    def _move_up(self) -> None:
        """
        Move the cursor to point the upper tile from the current tile
        """
        if not self._has_upper_tile():
            raise RuntimeError("There is no upper tile to move.")

        self._cursor[1] -= 1

    def _has_lower_tile(self) -> bool:
        """
        Check if there is the lower tile from the cursor.
        :return: True if it has, False otherwise
        """
        return self._cursor[1] < self._y_num_tiles - 1

    def _move_down(self) -> None:
        """
        Move the cursor to point the ㅣㅐㅈㄷ tile from the current tile
        """
        if not self._has_lower_tile():
            raise RuntimeError("There is no lower tile to move.")
        self._cursor[1] += 1

    def _has_left_tile(self) -> bool:
        """
        Check if there is left tile from the cursor.
        :return: True if it has, False otherwise
        """
        return self._cursor[0] > 0

    def _move_left(self) -> None:
        """
        Move the cursor to point the left tile from the current tile
        """
        if not self._has_left_tile():
            raise RuntimeError("There is no left tile to move.")

        self._cursor[0] -= 1

    def _has_right_tile(self) -> bool:
        """
        Check if there is right tile from the cursor
        :return: True if it has, False otherwise
        """
        return self._cursor[0] < self._x_num_tiles - 1

    def _move_right(self) -> None:
        """
        Move the cursor to point the right tile from the current tile
        """
        if not self._has_right_tile():
            raise RuntimeError("There is no right tile to move.")

        self._cursor[0] += 1

    def _get_tile(self) -> Tile:
        """
        Returns the tile that is pointed by the cursor
        :return: the tile
        """
        return self._board[self._cursor[0]][self._cursor[1]]

    def _get_upper_tile(self) -> Tile:
        """
        Returns the upper tile from the cursor.
        :return: the tile
        """
        if not self._has_upper_tile():
            raise RuntimeError("There is no upper tile to get.")

        return self._board[self._cursor[0]][self._cursor[1] - 1]

    def _get_lower_tile(self) -> Tile:
        """
        Returns the lower tile from the cursor.
        :return: the tile
        """
        if not self._has_lower_tile():
            raise RuntimeError("There is no lower tile to get.")

        return self._board[self._cursor[0]][self._cursor[1] + 1]

    def _get_left_tile(self) -> Tile:
        """
        Returns the left tile from the cursor.
        :return: the tile
        """
        if not self._has_left_tile():
            raise RuntimeError("There is no left tile to get.")

        return self._board[self._cursor[0] - 1][self._cursor[1]]

    def _get_right_tile(self) -> Tile:
        """
        Returns the right tile from the cursor.
        :return: the tile
        """
        if not self._has_right_tile():
            raise RuntimeError("There is no right tile to get.")

        return self._board[self._cursor[0] + 1][self._cursor[1]]

    def un_solve(self) -> None:
        """
        Un-solve the maze so that it can be solved again.
        """
        self._cursor[0] = 0
        self._cursor[1] = 0

        for i in range(self._x_num_tiles):
            for j in range(self._y_num_tiles):
                tile = self._board[i][j]

                if tile.is_path() or tile.is_start() or tile.is_goal():
                    tile.validate()
                    tile.un_visit()

    def reset(self) -> None:
        """
        Reset the maze including the path created by user
        """
        self._cursor[0] = 0
        self._cursor[1] = 0

        for i in range(self._x_num_tiles):
            for j in range(self._y_num_tiles):
                tile = self._board[i][j]
                tile.reset()
