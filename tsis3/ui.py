import pygame
from persistence import load_leaderboard, save_settings

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (0, 0, 255)


def draw_button(screen, text, x, y, w, h, font):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

    return rect


def main_menu(screen):
    font = pygame.font.SysFont("Verdana", 25)

    while True:
        screen.fill(WHITE)

        title = font.render("Racer Game", True, BLACK)
        screen.blit(title, (120, 80))

        play_btn = draw_button(screen, "Play", 100, 180, 200, 50, font)
        leaderboard_btn = draw_button(screen, "Leaderboard", 100, 250, 200, 50, font)
        settings_btn = draw_button(screen, "Settings", 100, 320, 200, 50, font)
        quit_btn = draw_button(screen, "Quit", 100, 390, 200, 50, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    return "play"
                if leaderboard_btn.collidepoint(event.pos):
                    return "leaderboard"
                if settings_btn.collidepoint(event.pos):
                    return "settings"
                if quit_btn.collidepoint(event.pos):
                    return "quit"


def get_username(screen):
    font = pygame.font.SysFont("Verdana", 25)
    name = ""

    while True:
        screen.fill(WHITE)

        text = font.render("Enter name:", True, BLACK)
        screen.blit(text, (100, 180))

        name_text = font.render(name, True, BLUE)
        screen.blit(name_text, (100, 230))

        hint = font.render("Press ENTER", True, BLACK)
        screen.blit(hint, (100, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Player"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name == "":
                        return "Player"
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 10:
                        name += event.unicode


def leaderboard_screen(screen):
    font = pygame.font.SysFont("Verdana", 22)
    small_font = pygame.font.SysFont("Verdana", 18)

    leaderboard = load_leaderboard()

    while True:
        screen.fill(WHITE)

        title = font.render("Top 10 Leaderboard", True, BLACK)
        screen.blit(title, (70, 40))

        y = 100

        if len(leaderboard) == 0:
            empty = small_font.render("No scores yet", True, BLACK)
            screen.blit(empty, (130, y))
        else:
            for i, item in enumerate(leaderboard):
                line = f"{i + 1}. {item['name']} | score: {item['score']} | dist: {item['distance']}"
                text = small_font.render(line, True, BLACK)
                screen.blit(text, (20, y))
                y += 35

        back_btn = draw_button(screen, "Back", 100, 520, 200, 50, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return


def settings_screen(screen, settings):
    font = pygame.font.SysFont("Verdana", 22)

    colors = ["blue", "red", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        title = font.render("Settings", True, BLACK)
        screen.blit(title, (140, 60))

        sound_btn = draw_button(
            screen,
            "Sound: " + str(settings["sound"]),
            80, 150, 240, 50, font
        )

        color_btn = draw_button(
            screen,
            "Car color: " + settings["car_color"],
            80, 230, 240, 50, font
        )

        diff_btn = draw_button(
            screen,
            "Difficulty: " + settings["difficulty"],
            80, 310, 240, 50, font
        )

        back_btn = draw_button(screen, "Back", 80, 450, 240, 50, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                if color_btn.collidepoint(event.pos):
                    index = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(index + 1) % len(colors)]

                if diff_btn.collidepoint(event.pos):
                    index = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]

                if back_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return