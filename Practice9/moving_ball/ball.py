import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))
done = False
x = 30
y = 30

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP] and y - 25 >= 20:
        y -= 20
    if pressed[pygame.K_DOWN] and y + 25 <= 380:
        y += 20
    if pressed[pygame.K_LEFT] and x - 25 >= 20:
        x -= 20
    if pressed[pygame.K_RIGHT] and x + 25 <= 380:
        x += 20

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 25)

    pygame.display.flip()
    clock.tick(60)