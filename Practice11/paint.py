import pygame
import math

# Colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255)
}


def main():
    pygame.init()

    # Main screen
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")

    clock = pygame.time.Clock()

    # Font for help text
    font = pygame.font.SysFont("Arial", 18)

    # Separate surface where all drawings are saved
    canvas = pygame.Surface((640, 480))
    canvas.fill(BLACK)

    # Default settings
    radius = 15
    color = COLORS["blue"]
    tool = "pen"

    drawing = False
    start_pos = None
    last_pos = None

    while True:
        for event in pygame.event.get():

            # Close window
            if event.type == pygame.QUIT:
                return

            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # Color selection 
                if event.key == pygame.K_r:
                    color = COLORS["red"]
                elif event.key == pygame.K_g:
                    color = COLORS["green"]
                elif event.key == pygame.K_b:
                    color = COLORS["blue"]

                # Tool selection 
                elif event.key == pygame.K_p:
                    tool = "pen"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_q:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"

                # New tools
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_t:
                    tool = "right_triangle"
                elif event.key == pygame.K_y:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"

                # Size control 
                elif event.key == pygame.K_EQUALS:
                    radius += 1
                elif event.key == pygame.K_MINUS:
                    radius = max(1, radius - 1)

            # Start drawing when left mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
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
                        draw_rectangle(canvas, start_pos, end_pos, color, radius)

                    elif tool == "circle":
                        draw_circle(canvas, start_pos, end_pos, color, radius)

                    elif tool == "square":
                        draw_square(canvas, start_pos, end_pos, color, radius)

                    elif tool == "right_triangle":
                        draw_right_triangle(canvas, start_pos, end_pos, color, radius)

                    elif tool == "equilateral_triangle":
                        draw_equilateral_triangle(canvas, start_pos, end_pos, color, radius)

                    elif tool == "rhombus":
                        draw_rhombus(canvas, start_pos, end_pos, color, radius)

            # Draw pen or eraser while mouse is moving
            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == "pen":
                    pygame.draw.line(canvas, color, last_pos, event.pos, radius)
                    last_pos = event.pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, BLACK, last_pos, event.pos, radius)
                    last_pos = event.pos

        # Draw saved canvas
        screen.blit(canvas, (0, 0))

        # Preview shapes before releasing mouse
        if drawing and tool in [
            "rect",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ]:
            mouse_pos = pygame.mouse.get_pos()

            if tool == "rect":
                draw_rectangle(screen, start_pos, mouse_pos, color, radius)

            elif tool == "circle":
                draw_circle(screen, start_pos, mouse_pos, color, radius)

            elif tool == "square":
                draw_square(screen, start_pos, mouse_pos, color, radius)

            elif tool == "right_triangle":
                draw_right_triangle(screen, start_pos, mouse_pos, color, radius)

            elif tool == "equilateral_triangle":
                draw_equilateral_triangle(screen, start_pos, mouse_pos, color, radius)

            elif tool == "rhombus":
                draw_rhombus(screen, start_pos, mouse_pos, color, radius)

        # Show commands on screen
        draw_help(screen, font, tool, radius)

        pygame.display.flip()
        clock.tick(60)


def draw_help(screen, font, tool, radius):
    # Text with all available commands
    lines = [
        "Commands:",
        "R/G/B - colors",
        "P - pen | E - eraser",
        "Q - rectangle | C - circle",
        "S - square | T - right triangle",
        "Y - equilateral triangle | H - rhombus",
        "+ / - - change size",
        "ESC - exit",
        f"Current tool: {tool}",
        f"Size: {radius}"
    ]

    x = 10
    y = 10

    # Draw small black background for text
    pygame.draw.rect(screen, BLACK, (5, 5, 310, 210))

    # Draw every line of help text
    for line in lines:
        text = font.render(line, True, WHITE)
        screen.blit(text, (x, y))
        y += 22


def draw_rectangle(surface, start, end, color, width):
    # Get start and end coordinates
    x1, y1 = start
    x2, y2 = end

    # Create rectangle from any direction
    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    pygame.draw.rect(surface, color, rect, width)


def draw_circle(surface, start, end, color, width):
    # Center is the first mouse position
    x1, y1 = start
    x2, y2 = end

    # Distance between start and end is radius
    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

    pygame.draw.circle(surface, color, start, radius, width)


def draw_square(surface, start, end, color, width):
    # Square has equal width and height
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    # Determine direction
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
    # Right triangle is made from 3 points
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, start, end, color, width):
    # Equilateral triangle has all sides equal
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)

    # Height formula for equilateral triangle
    height = int((math.sqrt(3) / 2) * side)

    # Direction depends on mouse movement
    if y2 < y1:
        height = -height

    points = [
        (x1, y1),
        (x1 + side, y1),
        (x1 + side // 2, y1 + height)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, start, end, color, width):
    # Rhombus is drawn using 4 points
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