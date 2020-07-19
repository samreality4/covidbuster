import pygame
import os
import time
import random

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Covid Busters")


ENEMY = pygame.image.load(os.path.join("assets", "virus.png"))


RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

BG = pygame.image.load(os.path.join("assets", "background-black.png"))


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    def redraw_window():
        WINDOW.blit(BG, (100, 0))
        pygame.display.update()

    # FPS = frame per second
    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
