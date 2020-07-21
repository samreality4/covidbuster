import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Covid Busters")


RED_VIRUS = pygame.image.load(os.path.join("assets", "red-virus.png"))
BLUE_VIRUS = pygame.image.load(os.path.join("assets", "blue-virus.png"))
GREEN_VIRUS = pygame.image.load(os.path.join("assets", "green-virus.png"))


CELL = pygame.image.load(os.path.join("assets", "white_blood_cell.png"))


RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


class Cell:
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.cell_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.cell_img, (self.x, self.y))

    def get_width(self):
        return self.cell_img.get_width()

    def get_height(self):
        return self.cell_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(x, y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            #TODO x and y not defined


class Player(Cell):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.cell_img = CELL
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.cell_img)
        self.max_health = health


class Enemy(Cell):
    COLOR_MAP = {
        "red": (RED_VIRUS, RED_LASER),
        "green": (GREEN_VIRUS, GREEN_LASER),
        "blue": (BLUE_VIRUS, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health=health)
        self.cell_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.cell_img)

    def move(self, vel):
        self.y += vel


class Laser(Cell):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y <= height and self.y >= 0

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    lost = False
    lost_count = 0

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5

    player = Player(WIDTH/2 - CELL.get_width()/2, 500)

    clock = pygame.time.Clock()

    def redraw_window():
        WINDOW.blit(BG, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render(
                "Take some vitamin pills and try again!!", 1, (255, 255, 255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    # FPS = frame per second
    while run:
        clock.tick(FPS)

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100),
                              random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x + player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y + player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        redraw_window()


main()
