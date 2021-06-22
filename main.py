import pygame
from maze import Maze

pygame.init()
pygame.display.set_caption("Maze Solver")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 720
HEIGHT = 720
FPS = 60

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
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if dragging and pygame.mouse.get_pressed(3)[0]:
                MAZE.left_click(pygame.mouse.get_pos())
            elif dragging and pygame.mouse.get_pressed(3)[2]:
                MAZE.right_click(pygame.mouse.get_pos())

            # check for keys pressed down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MAZE.reset()

                if event.key == pygame.K_SPACE:
                    MAZE.un_solve()
                    MAZE.solve()

        draw_display()


if __name__ == "__main__":
    main()
