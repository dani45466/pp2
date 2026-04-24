import pygame

BLACK = (0, 0, 0)
COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255)
}

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    canvas = pygame.Surface((640, 480))
    canvas.fill(BLACK)

    radius = 15
    color = COLORS["blue"]
    tool = "pen"

    drawing = False
    start_pos = None
    last_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # color selection
                if event.key == pygame.K_r:
                    color = COLORS["red"]
                elif event.key == pygame.K_g:
                    color = COLORS["green"]
                elif event.key == pygame.K_b:
                    color = COLORS["blue"]

                # tool selection
                elif event.key == pygame.K_p:
                    tool = "pen"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_q:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"

                # size
                elif event.key == pygame.K_EQUALS:
                    radius += 1
                elif event.key == pygame.K_MINUS:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    if tool == "rect":
                        draw_rectangle(canvas, start_pos, end_pos, color, radius)

                    elif tool == "circle":
                        draw_circle(canvas, start_pos, end_pos, color, radius)

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == "pen":
                    pygame.draw.line(canvas, color, last_pos, event.pos, radius)
                    last_pos = event.pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, BLACK, last_pos, event.pos, radius)
                    last_pos = event.pos

        screen.blit(canvas, (0, 0))

        # preview rectangle/circle before releasing mouse
        if drawing and tool in ["rect", "circle"]:
            mouse_pos = pygame.mouse.get_pos()
            if tool == "rect":
                draw_rectangle(screen, start_pos, mouse_pos, color, radius)
            elif tool == "circle":
                draw_circle(screen, start_pos, mouse_pos, color, radius)

        pygame.display.flip()
        clock.tick(60)


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

    radius = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5)

    pygame.draw.circle(surface, color, start, radius, width)


main()