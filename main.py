import concurrent.futures
import sys
from tkinter import Tk
from tkinter.messagebox import showinfo, askyesno, askretrycancel

import pygame

from maze import Maze

Tk().withdraw()  # don't display the tk window to only use messageboxes

pygame.init()
pygame.display.set_caption("Maze Solver")

BLACK = (0, 0, 0)

WIDTH = 720
HEIGHT = 720
FPS = 60

print(askretrycancel("test", "test"))

MAZE_SIZE = (20, 20)

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
MAZE = Maze(DISPLAY, MAZE_SIZE)


def draw_display():
    DISPLAY.fill(BLACK)
    MAZE.draw()
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    dragging = False

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if dragging and pygame.mouse.get_pressed(3)[0]:
                MAZE.left_click(pygame.mouse.get_pos())
            elif dragging and pygame.mouse.get_pressed(3)[2]:
                MAZE.right_click(pygame.mouse.get_pos())

            # check for keys pressed down
            if event.type == pygame.KEYDOWN:
                # reset the maze
                if event.key == pygame.K_ESCAPE:
                    MAZE.reset()

                # solve the maze
                if event.key == pygame.K_SPACE:
                    show_step = askyesno(message="Show step?")

                    MAZE.un_solve()
                    future = MAZE.solve(show_step)

                    for f in concurrent.futures.as_completed([future]):
                        found_path = f.result()

                        if not found_path:
                            showinfo("Result", "Path Not Found!")

        draw_display()


if __name__ == "__main__":
    showinfo("Instruction", "• The red tile in the top-left corner is the start point.\n"
                            "• The red tile in the bottom-right corner is the goal.\n"
                            "• The black tiles are the walls.\n"
                            "• The grey tiles represent that they have been visited but decided not to be a correct path.\n"
                            "• Hold left-click and drag to create paths for the maze. It will be represented as white.\n"
                            "• To delete the path, hold right-click and drag.\n"
                            "• Press space to solve the maze.\n"
                            "• The solution will be represented as green. Moving diagonally is not allowed.\n"
                            "• Press escape to reset the solution and clear the drawn paths.")
    main()
