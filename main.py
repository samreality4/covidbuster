import pygame
import os
import time
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Covid Busters")


pygame.mixer.music.load(os.path.join("assets", "bgmusic.ogg"))
pygame.mixer.music.play(-1)

RED_VIRUS = pygame.image.load(os.path.join("assets", "red_virus.png"))
BLUE_VIRUS = pygame.image.load(os.path.join("assets", "blue_virus.png"))
GREEN_VIRUS = pygame.image.load(os.path.join("assets", "green_virus.png"))

CELL = pygame.image.load(os.path.join("assets", "white_blood_cell.png"))

RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

OMEGA_LASER = pygame.image.load(
    os.path.join("assets", "omega.png"))

LASER_SOUND = pygame.mixer.Sound(os.path.join("assets", "regular_laser.wav"))
OMEGA_LASER_SOUND = pygame.mixer.Sound(
    os.path.join("assets", "omega_laser.wav"))
DESTROYED_SOUND = pygame.mixer.Sound(
    os.path.join("assets", "pop.wav"))

BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-red.jpg")), (WIDTH, HEIGHT))


###############################

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
        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.cell_img.get_width()

    def get_height(self):
        return self.cell_img.get_height()

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


###############################


class Player(Cell):
    OMEGA_COOLDOWN = 80

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.cell_img = CELL
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.cell_img)
        self.max_health = health
        self.omega_laser_img = OMEGA_LASER
        self.omega_cool_down_counter = 0

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            pygame.mixer.Sound.play(LASER_SOUND)
            self.cool_down_counter = 1

    def shoot_omega(self):
        if self.omega_cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.omega_laser_img)
            self.lasers.append(laser)
            pygame.mixer.Sound.play(OMEGA_LASER_SOUND)
            self.omega_cool_down_counter = 1

    def omega_cooldown(self):
        if self.omega_cool_down_counter >= self.OMEGA_COOLDOWN:
            self.omega_cool_down_counter = 0
        elif self.omega_cool_down_counter > 0:
            self.omega_cool_down_counter += 1

    def move_lasers(self, vel, objs):
        self.cooldown()
        self.omega_cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        pygame.mixer.Sound.play(DESTROYED_SOUND)
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                                               self.cell_img.get_height() + 10, self.cell_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.cell_img.get_height() +
                                               10, self.cell_img.get_width() * (self.health/self.max_health), 10))

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

###############################


class Enemy(Cell):
    COLOR_MAP = {
        "red": (RED_VIRUS, RED_LASER),
        "green": (GREEN_VIRUS, GREEN_LASER),
        "blue": (BLUE_VIRUS, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=10):
        super().__init__(x, y, health=health)
        self.cell_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.cell_img)

    def move(self, vel):
        self.y += vel

###############################


class Laser:
    def __init__(self, x, y, img):
        self.x = x - 25
        self.y = y - 50
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

###############################


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

    laser_vel = 5

    player = Player(int(WIDTH/2 - CELL.get_width()/2), 500)

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
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 200))

        pygame.display.update()

    # FPS = frame per second
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 5:
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
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_z]:
            player.shoot_omega()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                pygame.mixer.Sound.play(DESTROYED_SOUND)
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 60)
    run = True

    while run:
        WINDOW.blit(BG, (0, 0))
        title_label = title_font.render(
            "Press the mouse to begin...", 1, (255, 255, 255))
        WINDOW.blit(
            title_label, (int(WIDTH/2 - title_label.get_width()/2), 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
