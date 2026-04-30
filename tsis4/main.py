import pygame
import random
import sys
import json
import os

import db


pygame.init()

# ---------- Settings ----------
WIDTH = 600
HEIGHT = 420
CELL_SIZE = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game TSIS 4")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 40)

# ---------- Colors ----------
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
DARK_RED = (120, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 0)
ORANGE = (255, 150, 0)
BLUE = (0, 120, 255)
PURPLE = (160, 0, 255)
CYAN = (0, 255, 255)

wall_thickness = CELL_SIZE

SETTINGS_FILE = "settings.json"


# ---------- Load / Save Settings ----------
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "snake_color": [0, 200, 0],
            "grid": True,
            "sound": True
        }

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


settings = load_settings()


# ---------- Database ----------
try:
    db.create_tables()
except Exception as error:
    print("Database error:", error)


# ---------- Buttons ----------
def draw_text(text, x, y, color=WHITE, use_big=False):
    if use_big:
        img = big_font.render(text, True, color)
    else:
        img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_button(text, rect):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)

    img = font.render(text, True, WHITE)
    screen.blit(img, (rect.x + 15, rect.y + 10))


def button_clicked(rect, event):
    return event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos)


# ---------- Screens ----------
def main_menu():
    username = ""

    play_btn = pygame.Rect(210, 150, 180, 45)
    leaderboard_btn = pygame.Rect(210, 205, 180, 45)
    settings_btn = pygame.Rect(210, 260, 180, 45)
    quit_btn = pygame.Rect(210, 315, 180, 45)

    while True:
        screen.fill(BLACK)

        draw_text("Snake Game", 190, 40, GREEN, True)
        draw_text("Enter username:", 190, 95)
        draw_text(username, 190, 120, YELLOW)

        draw_button("Play", play_btn)
        draw_button("Leaderboard", leaderboard_btn)
        draw_button("Settings", settings_btn)
        draw_button("Quit", quit_btn)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username != "":
                        game_loop(username)
                else:
                    if len(username) < 12:
                        username += event.unicode

            if button_clicked(play_btn, event):
                if username != "":
                    game_loop(username)

            if button_clicked(leaderboard_btn, event):
                leaderboard_screen()

            if button_clicked(settings_btn, event):
                settings_screen()

            if button_clicked(quit_btn, event):
                quit_game()


def leaderboard_screen():
    back_btn = pygame.Rect(220, 350, 160, 45)

    try:
        top_scores = db.get_top_10()
    except Exception:
        top_scores = []

    while True:
        screen.fill(BLACK)

        draw_text("Leaderboard TOP 10", 150, 30, YELLOW, True)

        y = 90
        draw_text("Rank   Name        Score   Level", 90, y)
        y += 35

        rank = 1
        for row in top_scores:
            username, score, level, date = row
            draw_text(f"{rank}.     {username[:10]:10}  {score:5}   {level}", 90, y)
            y += 25
            rank += 1

        draw_button("Back", back_btn)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if button_clicked(back_btn, event):
                return


def settings_screen():
    global settings

    grid_btn = pygame.Rect(180, 120, 240, 45)
    sound_btn = pygame.Rect(180, 180, 240, 45)
    color_btn = pygame.Rect(180, 240, 240, 45)
    back_btn = pygame.Rect(180, 310, 240, 45)

    colors = [
        [0, 200, 0],
        [255, 255, 0],
        [0, 120, 255],
        [255, 0, 255]
    ]

    color_index = 0

    while True:
        screen.fill(BLACK)

        draw_text("Settings", 220, 40, YELLOW, True)

        draw_button(f"Grid: {settings['grid']}", grid_btn)
        draw_button(f"Sound: {settings['sound']}", sound_btn)
        draw_button("Change Snake Color", color_btn)
        draw_button("Save & Back", back_btn)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if button_clicked(grid_btn, event):
                settings["grid"] = not settings["grid"]

            if button_clicked(sound_btn, event):
                settings["sound"] = not settings["sound"]

            if button_clicked(color_btn, event):
                color_index += 1
                if color_index >= len(colors):
                    color_index = 0
                settings["snake_color"] = colors[color_index]

            if button_clicked(back_btn, event):
                save_settings(settings)
                return


def game_over_screen(username, score, level, best):
    retry_btn = pygame.Rect(210, 245, 180, 45)
    menu_btn = pygame.Rect(210, 305, 180, 45)

    try:
        db.save_result(username, score, level)
        best = max(best, score)
    except Exception as error:
        print("Save error:", error)

    while True:
        screen.fill(BLACK)

        draw_text("Game Over", 190, 60, RED, True)
        draw_text(f"Final Score: {score}", 200, 130)
        draw_text(f"Level Reached: {level}", 200, 165)
        draw_text(f"Personal Best: {best}", 200, 200)

        draw_button("Retry", retry_btn)
        draw_button("Main Menu", menu_btn)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if button_clicked(retry_btn, event):
                game_loop(username)

            if button_clicked(menu_btn, event):
                return


# ---------- Game Helpers ----------
def draw_walls():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, wall_thickness))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - wall_thickness, WIDTH, wall_thickness))
    pygame.draw.rect(screen, GRAY, (0, 0, wall_thickness, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - wall_thickness, 0, wall_thickness, HEIGHT))


def draw_grid():
    if not settings["grid"]:
        return

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))


def check_wall_collision(head):
    x, y = head

    if x < wall_thickness:
        return True
    if x >= WIDTH - wall_thickness:
        return True
    if y < wall_thickness:
        return True
    if y >= HEIGHT - wall_thickness:
        return True

    return False


def random_position(snake, obstacles):
    while True:
        x = random.randrange(wall_thickness, WIDTH - wall_thickness, CELL_SIZE)
        y = random.randrange(wall_thickness, HEIGHT - wall_thickness, CELL_SIZE)

        pos = (x, y)

        if pos not in snake and pos not in obstacles:
            return pos


def generate_food(snake, obstacles):
    food_types = [
        {"weight": 1, "color": RED},
        {"weight": 2, "color": YELLOW},
        {"weight": 3, "color": ORANGE}
    ]

    food_type = random.choice(food_types)

    return {
        "position": random_position(snake, obstacles),
        "weight": food_type["weight"],
        "color": food_type["color"],
        "spawn_time": pygame.time.get_ticks()
    }


def generate_poison(snake, obstacles):
    return {
        "position": random_position(snake, obstacles),
        "spawn_time": pygame.time.get_ticks()
    }


def generate_power_up(snake, obstacles):
    power_types = ["speed", "slow", "shield"]
    power_type = random.choice(power_types)

    return {
        "position": random_position(snake, obstacles),
        "type": power_type,
        "spawn_time": pygame.time.get_ticks()
    }


def generate_obstacles(level, snake):
    obstacles = []

    if level < 3:
        return obstacles

    count = level + 2
    head = snake[0]

    safe_positions = [
        head,
        (head[0] + CELL_SIZE, head[1]),
        (head[0] - CELL_SIZE, head[1]),
        (head[0], head[1] + CELL_SIZE),
        (head[0], head[1] - CELL_SIZE)
    ]

    while len(obstacles) < count:
        x = random.randrange(wall_thickness, WIDTH - wall_thickness, CELL_SIZE)
        y = random.randrange(wall_thickness, HEIGHT - wall_thickness, CELL_SIZE)
        pos = (x, y)

        if pos not in snake and pos not in obstacles and pos not in safe_positions:
            obstacles.append(pos)

    return obstacles


def draw_snake(snake):
    snake_color = tuple(settings["snake_color"])

    for part in snake:
        pygame.draw.rect(screen, snake_color, (part[0], part[1], CELL_SIZE, CELL_SIZE))


def draw_food(food):
    x, y = food["position"]
    pygame.draw.rect(screen, food["color"], (x, y, CELL_SIZE, CELL_SIZE))

    weight_text = font.render(str(food["weight"]), True, BLACK)
    screen.blit(weight_text, (x + 8, y + 2))


def draw_poison(poison):
    if poison is None:
        return

    x, y = poison["position"]
    pygame.draw.rect(screen, DARK_RED, (x, y, CELL_SIZE, CELL_SIZE))
    draw_text("P", x + 7, y + 1, WHITE)


def draw_power_up(power_up):
    if power_up is None:
        return

    x, y = power_up["position"]

    if power_up["type"] == "speed":
        color = BLUE
        letter = "F"
    elif power_up["type"] == "slow":
        color = CYAN
        letter = "S"
    else:
        color = PURPLE
        letter = "H"

    pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
    draw_text(letter, x + 7, y + 1, WHITE)


def draw_obstacles(obstacles):
    for block in obstacles:
        pygame.draw.rect(screen, GRAY, (block[0], block[1], CELL_SIZE, CELL_SIZE))


def draw_info(score, level, best, active_power):
    draw_text(f"Score: {score}", 20, 8)
    draw_text(f"Level: {level}", 150, 8)
    draw_text(f"Best: {best}", 270, 8)

    if active_power is not None:
        draw_text(f"Power: {active_power}", 400, 8, YELLOW)


# ---------- Main Game ----------
def game_loop(username):
    snake = [(300, 210), (270, 210), (240, 210)]
    direction = (CELL_SIZE, 0)

    score = 0
    level = 1
    speed = 5

    food_lifetime = 5000
    power_lifetime = 8000
    power_duration = 5000

    obstacles = []
    food = generate_food(snake, obstacles)
    poison = generate_poison(snake, obstacles)

    power_up = None
    power_spawn_time = pygame.time.get_ticks()

    active_power = None
    active_power_start = 0
    shield = False

    try:
        best = db.get_personal_best(username)
    except Exception:
        best = 0

    while True:
        current_time = pygame.time.get_ticks()

        # ---------- Events ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        # ---------- Food timer ----------
        if current_time - food["spawn_time"] > food_lifetime:
            food = generate_food(snake, obstacles)

        # ---------- Power-up spawn ----------
        if power_up is None and current_time - power_spawn_time > 7000:
            power_up = generate_power_up(snake, obstacles)

        if power_up is not None:
            if current_time - power_up["spawn_time"] > power_lifetime:
                power_up = None
                power_spawn_time = current_time

        # ---------- Active power timer ----------
        if active_power in ["speed", "slow"]:
            if current_time - active_power_start > power_duration:
                active_power = None

        # ---------- Move snake ----------
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        hit_wall = check_wall_collision(new_head)
        hit_self = new_head in snake
        hit_obstacle = new_head in obstacles

        if hit_wall or hit_self or hit_obstacle:
            if shield:
                shield = False
                active_power = None

                # Do not move into dangerous cell
                new_head = snake[0]
            else:
                game_over_screen(username, score, level, best)
                return

        snake.insert(0, new_head)

        # ---------- Eat normal food ----------
        if new_head == food["position"]:
            score += food["weight"]

            old_level = level
            level = score // 3 + 1

            if level > old_level:
                speed += 1
                obstacles = generate_obstacles(level, snake)

            food = generate_food(snake, obstacles)

        # ---------- Eat poison ----------
        elif poison is not None and new_head == poison["position"]:
            if len(snake) <= 3:
                game_over_screen(username, score, level, best)
                return

            snake.pop()
            snake.pop()

            poison = generate_poison(snake, obstacles)

        # ---------- Eat power-up ----------
        elif power_up is not None and new_head == power_up["position"]:
            active_power = power_up["type"]
            active_power_start = current_time

            if active_power == "shield":
                shield = True

            power_up = None
            power_spawn_time = current_time

        else:
            snake.pop()

        # ---------- Speed effects ----------
        current_speed = speed

        if active_power == "speed":
            current_speed = speed + 4

        if active_power == "slow":
            current_speed = max(2, speed - 3)

        # ---------- Drawing ----------
        screen.fill(BLACK)

        draw_grid()
        draw_walls()
        draw_obstacles(obstacles)
        draw_snake(snake)
        draw_food(food)
        draw_poison(poison)
        draw_power_up(power_up)
        draw_info(score, level, best, active_power)

        pygame.display.update()
        clock.tick(current_speed)


def quit_game():
    pygame.quit()
    sys.exit()


main_menu()