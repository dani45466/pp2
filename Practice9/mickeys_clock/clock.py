import pygame
import sys
from datetime import datetime

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()


clock_img = pygame.image.load("images/clock.png").convert_alpha()
clock_img = pygame.transform.scale(clock_img, (400, 400))


hand_img = pygame.image.load("images/mickey_hand.png").convert_alpha()
hand_img = pygame.transform.scale(hand_img, (120, 120))


left_hand_img = pygame.transform.flip(hand_img, True, False)


center_x = WIDTH // 2
center_y = HEIGHT // 2

clock_rect = clock_img.get_rect(center=(center_x, center_y))

def draw_rotated_hand(image, angle, x, y):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=(x, y))
    screen.blit(rotated, rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    now = datetime.now()
    minutes = now.minute
    seconds = now.second

    minute_angle = -minutes * 6
    second_angle = -seconds * 6

    screen.fill((255, 255, 255))

    
    screen.blit(clock_img, clock_rect)

    
    draw_rotated_hand(hand_img, minute_angle, center_x, center_y)
    draw_rotated_hand(left_hand_img, second_angle, center_x, center_y)

    pygame.display.update()
    clock.tick(1)