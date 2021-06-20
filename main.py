import pygame
from maze import Maze

pygame.init()
pygame.display.set_caption("Maze Solver")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 720
HEIGHT = 720
FPS = 60

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
MAZE = Maze(DISPLAY, (50, 50))


def draw_display():
    DISPLAY.fill(WHITE)
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

            if dragging:
                MAZE.click(pygame.mouse.get_pos())

            if event.type == pygame.K_ESCAPE:
                MAZE.reset()

            if event.type == pygame.K_RETURN:
                MAZE.solve()

        draw_display()


if __name__ == "__main__":
    main()
