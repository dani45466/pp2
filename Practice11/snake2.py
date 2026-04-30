import pygame
import random
import sys

pygame.init()

# ---------- Settings ----------
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

# ---------- Colors ----------
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 0)
ORANGE = (255, 150, 0)

# ---------- Game variables ----------
snake = [(300, 210), (270, 210), (240, 210)]
direction = (CELL_SIZE, 0)

score = 0
level = 1
speed = 2

# Borders / walls
wall_thickness = CELL_SIZE

# ---------- Food settings ----------
# Different food weights.
# weight means how many points the player gets.
FOOD_TYPES = [
    {"weight": 1, "color": RED},
    {"weight": 2, "color": YELLOW},
    {"weight": 3, "color": ORANGE}
]

# Food disappears after this time in milliseconds
FOOD_LIFETIME = 5000


def draw_walls():
    """Draw borders around the playing area."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, wall_thickness))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - wall_thickness, WIDTH, wall_thickness))
    pygame.draw.rect(screen, GRAY, (0, 0, wall_thickness, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - wall_thickness, 0, wall_thickness, HEIGHT))


def generate_food():
    """
    Generate food in random position.
    Food must not appear on wall or inside snake.
    Also food gets random weight and color.
    """
    while True:
        x = random.randrange(wall_thickness, WIDTH - wall_thickness, CELL_SIZE)
        y = random.randrange(wall_thickness, HEIGHT - wall_thickness, CELL_SIZE)

        food_position = (x, y)

        if food_position not in snake:
            # Choose random food type
            food_type = random.choice(FOOD_TYPES)

            return {
                "position": food_position,
                "weight": food_type["weight"],
                "color": food_type["color"],
                "spawn_time": pygame.time.get_ticks()
            }


food = generate_food()


def draw_snake():
    """Draw every part of the snake."""
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL_SIZE, CELL_SIZE))


def draw_food():
    """Draw food with its own color."""
    x, y = food["position"]
    pygame.draw.rect(screen, food["color"], (x, y, CELL_SIZE, CELL_SIZE))

    # Show food weight on food
    weight_text = font.render(str(food["weight"]), True, BLACK)
    screen.blit(weight_text, (x + 8, y + 2))


def draw_score_and_level():
    """Show score and level on the screen."""
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (25, 25))


def check_wall_collision(head):
    """Check if snake hits the border."""
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


def game_over():
    """Show game over message and close the game."""
    screen.fill(BLACK)

    text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)

    screen.blit(text, (WIDTH // 2 - 70, HEIGHT // 2 - 30))
    screen.blit(score_text, (WIDTH // 2 - 85, HEIGHT // 2 + 10))

    pygame.display.update()
    pygame.time.delay(2000)

    pygame.quit()
    sys.exit()


# ---------- Main game loop ----------
while True:
    # ---------- Events ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Change direction with keyboard
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
    # If food stays too long, it disappears and new food appears
    current_time = pygame.time.get_ticks()
    if current_time - food["spawn_time"] > FOOD_LIFETIME:
        food = generate_food()

    # ---------- Move snake ----------
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # Check wall collision
    if check_wall_collision(new_head):
        game_over()

    # Check collision with itself
    if new_head in snake:
        game_over()

    # Add new head
    snake.insert(0, new_head)

    # ---------- Food collision ----------
    if new_head == food["position"]:
        # Add score depending on food weight
        score += food["weight"]

        # Every 3 points level increases
        if score % 3 == 0:
            level += 1
            speed += 1

        food = generate_food()
    else:
        # If food is not eaten, remove tail
        snake.pop()

    # ---------- Drawing ----------
    screen.fill(BLACK)

    draw_walls()
    draw_snake()
    draw_food()
    draw_score_and_level()

    pygame.display.update()

    clock.tick(speed)