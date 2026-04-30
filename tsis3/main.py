import pygame
import sys
import random
import time

from pygame.locals import *
from persistence import load_settings, save_score
from ui import main_menu, get_username, leaderboard_screen, settings_screen

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (90, 90, 90)
YELLOW = (255, 255, 0)
ORANGE = (255, 160, 0)
PURPLE = (160, 0, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

font = pygame.font.SysFont("Verdana", 45)
font_small = pygame.font.SysFont("Verdana", 18)

background = pygame.image.load("raceimages/AnimatedStreet.png")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load("raceimages/Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), -120)

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("raceimages/Coin.png")
        self.reset_coin()

    def reset_coin(self):
        self.weight = random.randint(1, 3)

        if self.weight == 1:
            size = 30
        elif self.weight == 2:
            size = 40
        else:
            size = 50

        self.image = pygame.transform.scale(self.original_image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), -50)

    def move(self):
        self.rect.move_ip(0, 7)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset_coin()


class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.original_image = pygame.image.load("raceimages/Player.png")
        self.image = pygame.transform.scale(self.original_image, (50, 100))

        # Simple color setting: draw colored rectangle on top of car
        if color_name == "red":
            pygame.draw.rect(self.image, RED, (10, 10, 30, 30))
        elif color_name == "green":
            pygame.draw.rect(self.image, GREEN, (10, 10, 30, 30))
        else:
            pygame.draw.rect(self.image, BLUE, (10, 10, 30, 30))

        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((60, 35))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(60, SCREEN_WIDTH - 60), random.randint(-700, -150))

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()


class Oil(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((55, 35))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(60, SCREEN_WIDTH - 60), random.randint(-900, -250))

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()


class MovingBarrier(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((80, 25))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.x_speed = 3
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(80, SCREEN_WIDTH - 80), random.randint(-1000, -300))

    def move(self):
        self.rect.move_ip(self.x_speed, self.speed)

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_speed *= -1

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.kind = "nitro"
        self.image = pygame.Surface((35, 35))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.kind = random.choice(["nitro", "shield", "repair"])

        if self.kind == "nitro":
            self.image.fill(YELLOW)
        elif self.kind == "shield":
            self.image.fill(BLUE)
        else:
            self.image.fill(GREEN)

        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), random.randint(-1200, -400))

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()


def draw_text(text, x, y, color=BLACK):
    label = font_small.render(text, True, color)
    DISPLAYSURF.blit(label, (x, y))


def game_over_screen(score, coins, distance):
    while True:
        DISPLAYSURF.fill(RED)

        title = font.render("Game Over", True, BLACK)
        DISPLAYSURF.blit(title, (60, 120))

        draw_text("Score: " + str(score), 120, 230)
        draw_text("Coins: " + str(coins), 120, 260)
        draw_text("Distance: " + str(distance), 120, 290)

        retry_rect = pygame.Rect(100, 370, 200, 50)
        menu_rect = pygame.Rect(100, 440, 200, 50)

        pygame.draw.rect(DISPLAYSURF, WHITE, retry_rect)
        pygame.draw.rect(DISPLAYSURF, WHITE, menu_rect)

        retry_text = font_small.render("Retry", True, BLACK)
        menu_text = font_small.render("Main Menu", True, BLACK)

        DISPLAYSURF.blit(retry_text, (175, 385))
        DISPLAYSURF.blit(menu_text, (145, 455))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return "retry"

                if menu_rect.collidepoint(event.pos):
                    return "menu"


def run_game(username, settings):
    SCORE = 0
    MON = 0
    distance = 0

    if settings["difficulty"] == "easy":
        speed = 4
        obstacle_count = 1
    elif settings["difficulty"] == "hard":
        speed = 7
        obstacle_count = 3
    else:
        speed = 5
        obstacle_count = 2

    N = 5
    last_speed_level = 0

    shield = False
    active_power = "none"
    power_end_time = 0

    P1 = Player(settings["car_color"])
    C1 = Coin()

    enemies = pygame.sprite.Group()
    enemies.add(Enemy(speed))

    obstacles = pygame.sprite.Group()

    for i in range(obstacle_count):
        obstacles.add(Obstacle(speed))

    oils = pygame.sprite.Group()
    oils.add(Oil(speed))

    barriers = pygame.sprite.Group()
    barriers.add(MovingBarrier(speed))

    powerups = pygame.sprite.Group()
    powerups.add(PowerUp(speed))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(C1)
    all_sprites.add(enemies)
    all_sprites.add(obstacles)
    all_sprites.add(oils)
    all_sprites.add(barriers)
    all_sprites.add(powerups)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        now = pygame.time.get_ticks()

        if active_power == "nitro" and now > power_end_time:
            active_power = "none"

        if active_power == "nitro":
            current_speed = speed + 3
        else:
            current_speed = speed

        # update speed for moving objects
        for enemy in enemies:
            enemy.speed = current_speed

        for obstacle in obstacles:
            obstacle.speed = current_speed

        for oil in oils:
            oil.speed = current_speed

        for barrier in barriers:
            barrier.speed = current_speed

        for power in powerups:
            power.speed = current_speed

        DISPLAYSURF.blit(background, (0, 0))

        distance += 1
        SCORE = distance // 20 + MON * 10

        # Draw info
        draw_text("Name: " + username, 10, 10)
        draw_text("Score: " + str(SCORE), 10, 35)
        draw_text("Coins: " + str(MON), 10, 60)
        draw_text("Distance: " + str(distance), 10, 85)

        if shield:
            draw_text("Shield: ON", 250, 10, BLUE)

        if active_power == "nitro":
            left = (power_end_time - now) // 1000
            draw_text("Nitro: " + str(left), 250, 35, ORANGE)

        # Move and draw
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        # Collect coin
        collected_coin = pygame.sprite.spritecollideany(P1, pygame.sprite.Group(C1))

        if collected_coin:
            MON += collected_coin.weight
            collected_coin.reset_coin()

            speed_level = MON // N

            if speed_level > last_speed_level:
                speed += 1
                last_speed_level = speed_level

                # difficulty scaling: add more traffic
                if len(enemies) < 4:
                    new_enemy = Enemy(speed)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)

        # Collect power-up
        collected_power = pygame.sprite.spritecollideany(P1, powerups)

        if collected_power:
            if collected_power.kind == "nitro":
                active_power = "nitro"
                power_end_time = now + 4000

            elif collected_power.kind == "shield":
                shield = True
                active_power = "shield"

            elif collected_power.kind == "repair":
                # repair clears one obstacle
                for obstacle in obstacles:
                    obstacle.reset()
                    break
                active_power = "repair"

            collected_power.reset()

        # Oil slows player down
        if pygame.sprite.spritecollideany(P1, oils):
            P1.rect.move_ip(0, 1)

        # Collisions
        hit_enemy = pygame.sprite.spritecollideany(P1, enemies)
        hit_obstacle = pygame.sprite.spritecollideany(P1, obstacles)
        hit_barrier = pygame.sprite.spritecollideany(P1, barriers)

        if hit_enemy or hit_obstacle or hit_barrier:
            if shield:
                shield = False

                if hit_enemy:
                    hit_enemy.reset()

                if hit_obstacle:
                    hit_obstacle.reset()

                if hit_barrier:
                    hit_barrier.reset()

            else:
                save_score(username, SCORE, MON, distance)
                result = game_over_screen(SCORE, MON, distance)
                return result

        pygame.display.update()
        FramePerSec.tick(FPS)


def main():
    settings = load_settings()

    while True:
        choice = main_menu(DISPLAYSURF)

        if choice == "play":
            username = get_username(DISPLAYSURF)

            while True:
                result = run_game(username, settings)

                if result == "retry":
                    continue

                if result == "menu":
                    break

                if result == "quit":
                    pygame.quit()
                    sys.exit()

        elif choice == "leaderboard":
            leaderboard_screen(DISPLAYSURF)

        elif choice == "settings":
            settings_screen(DISPLAYSURF, settings)

        elif choice == "quit":
            pygame.quit()
            sys.exit()


main()