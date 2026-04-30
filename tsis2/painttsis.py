import pygame
import math
from datetime import datetime
from collections import deque

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255)
}


def main():
    pygame.init()

    # Main screen
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")

    clock = pygame.time.Clock()

    # Font for help text and text tool
    font = pygame.font.SysFont("Arial", 18)
    text_font = pygame.font.SysFont("Arial", 28)

    # Separate surface where all drawings are saved
    canvas = pygame.Surface((640, 480))
    canvas.fill(BLACK)

    # Default settings
    brush_size = 5
    color = COLORS["blue"]
    tool = "pen"

    drawing = False
    start_pos = None
    last_pos = None

    # Text tool variables
    typing = False
    text_pos = None
    text_value = ""

    while True:
        for event in pygame.event.get():

            # Close window
            if event.type == pygame.QUIT:
                return

            # Keyboard controls
            if event.type == pygame.KEYDOWN:

                # If text mode is active
                if typing:
                    if event.key == pygame.K_RETURN:
                        text_surface = text_font.render(text_value, True, color)
                        canvas.blit(text_surface, text_pos)
                        typing = False
                        text_value = ""
                    elif event.key == pygame.K_v:
                        save_canvas(canvas)
                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                        text_value = ""

                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]

                    else:
                        text_value += event.unicode

                else:
                    if event.key == pygame.K_ESCAPE:
                        return

                    # Ctrl + S saves image
                    if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                        save_canvas(canvas)

                    # Color selection
                    elif event.key == pygame.K_r:
                        color = COLORS["red"]
                    elif event.key == pygame.K_g:
                        color = COLORS["green"]
                    elif event.key == pygame.K_b:
                        color = COLORS["blue"]
                    elif event.key == pygame.K_w:
                        color = COLORS["white"]

                    # Brush size selection
                    elif event.key == pygame.K_1:
                        brush_size = 2
                    elif event.key == pygame.K_2:
                        brush_size = 5
                    elif event.key == pygame.K_3:
                        brush_size = 10

                    # Tool selection
                    elif event.key == pygame.K_p:
                        tool = "pen"
                    elif event.key == pygame.K_e:
                        tool = "eraser"
                    elif event.key == pygame.K_q:
                        tool = "rect"
                    elif event.key == pygame.K_c:
                        tool = "circle"
                    elif event.key == pygame.K_l:
                        tool = "line"
                    elif event.key == pygame.K_f:
                        tool = "fill"
                    elif event.key == pygame.K_x:
                        tool = "text"

                    # Shape tools
                    elif event.key == pygame.K_s:
                        tool = "square"
                    elif event.key == pygame.K_t:
                        tool = "right_triangle"
                    elif event.key == pygame.K_y:
                        tool = "equilateral_triangle"
                    elif event.key == pygame.K_h:
                        tool = "rhombus"

            # Start drawing when left mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if tool == "fill":
                        flood_fill(canvas, event.pos, color)

                    elif tool == "text":
                        typing = True
                        text_pos = event.pos
                        text_value = ""

                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos

            # Finish drawing when left mouse button is released
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    # Draw final shape on canvas
                    if tool == "rect":
                        draw_rectangle(canvas, start_pos, end_pos, color, brush_size)

                    elif tool == "circle":
                        draw_circle(canvas, start_pos, end_pos, color, brush_size)

                    elif tool == "line":
                        pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

                    elif tool == "square":
                        draw_square(canvas, start_pos, end_pos, color, brush_size)

                    elif tool == "right_triangle":
                        draw_right_triangle(canvas, start_pos, end_pos, color, brush_size)

                    elif tool == "equilateral_triangle":
                        draw_equilateral_triangle(canvas, start_pos, end_pos, color, brush_size)

                    elif tool == "rhombus":
                        draw_rhombus(canvas, start_pos, end_pos, color, brush_size)

            # Draw pen or eraser while mouse is moving
            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == "pen":
                    pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                    last_pos = event.pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, BLACK, last_pos, event.pos, brush_size)
                    last_pos = event.pos

        # Draw saved canvas
        screen.blit(canvas, (0, 0))

        # Preview shapes before releasing mouse
        if drawing and tool in [
            "rect",
            "circle",
            "line",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ]:
            mouse_pos = pygame.mouse.get_pos()

            if tool == "rect":
                draw_rectangle(screen, start_pos, mouse_pos, color, brush_size)

            elif tool == "circle":
                draw_circle(screen, start_pos, mouse_pos, color, brush_size)

            elif tool == "line":
                pygame.draw.line(screen, color, start_pos, mouse_pos, brush_size)

            elif tool == "square":
                draw_square(screen, start_pos, mouse_pos, color, brush_size)

            elif tool == "right_triangle":
                draw_right_triangle(screen, start_pos, mouse_pos, color, brush_size)

            elif tool == "equilateral_triangle":
                draw_equilateral_triangle(screen, start_pos, mouse_pos, color, brush_size)

            elif tool == "rhombus":
                draw_rhombus(screen, start_pos, mouse_pos, color, brush_size)

        # Text preview
        if typing:
            text_surface = text_font.render(text_value, True, color)
            screen.blit(text_surface, text_pos)

            # Small cursor
            cursor_x = text_pos[0] + text_surface.get_width() + 2
            pygame.draw.line(screen, color, (cursor_x, text_pos[1]), (cursor_x, text_pos[1] + 28), 2)

        # Show commands on screen
        draw_help(screen, font, tool, brush_size, color)

        pygame.display.flip()
        clock.tick(60)


def save_canvas(canvas):
    # Save file with timestamp
    time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"paint_{time_now}.png"

    pygame.image.save(canvas, filename)
    print(f"Saved as {filename}")


def flood_fill(surface, pos, new_color):
    x, y = pos
    width, height = surface.get_size()

    old_color = surface.get_at((x, y))

    if old_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != old_color:
            continue

        surface.set_at((x, y), new_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def draw_help(screen, font, tool, brush_size, color):
    # Text with all available commands
    lines = [
        "Commands:",
        "R/G/B/W - colors",
        "1/2/3 - brush size",
        "P - pen | E - eraser",
        "Q - rectangle | C - circle",
        "L - line | F - fill",
        "X - text tool",
        "S - square | T - right triangle",
        "Y - equilateral triangle | H - rhombus",
        "Ctrl+S - save canvas",
        "ESC - exit",
        f"Current tool: {tool}",
        f"Brush size: {brush_size}",
        f"Color: {color}"
    ]

    x = 10
    y = 10

    # Draw small black background for text
    pygame.draw.rect(screen, BLACK, (5, 5, 360, 320))

    # Draw every line of help text
    for line in lines:
        text = font.render(line, True, WHITE)
        screen.blit(text, (x, y))
        y += 22


def draw_rectangle(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    pygame.draw.rect(surface, color, rect, width)


def draw_circle(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

    pygame.draw.circle(surface, color, start, radius, width)


def draw_square(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        side_x = -side
    else:
        side_x = side

    if y2 < y1:
        side_y = -side
    else:
        side_y = side

    rect = pygame.Rect(x1, y1, side_x, side_y)
    rect.normalize()

    pygame.draw.rect(surface, color, rect, width)


def draw_right_triangle(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)
    height = int((math.sqrt(3) / 2) * side)

    if y2 < y1:
        height = -height

    if x2 < x1:
        side = -side

    points = [
        (x1, y1),
        (x1 + side, y1),
        (x1 + side // 2, y1 + height)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


main()