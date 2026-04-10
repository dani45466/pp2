import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("Simple Music Player")

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

playlist = [
    "music/delorravision.mp3",
    "music/delorraendless.mp3",
    "music/муз1.mp3"
]

current = 0
playing = False


def play_music():
    global playing
    pygame.mixer.music.load(playlist[current])
    pygame.mixer.music.play()
    playing = True


def stop_music():
    global playing
    pygame.mixer.music.stop()
    playing = False


def next_music():
    global current
    current += 1
    if current >= len(playlist):
        current = 0
    play_music()


def previous_music():
    global current
    current -= 1
    if current < 0:
        current = len(playlist) - 1
    play_music()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_music()
            elif event.key == pygame.K_s:
                stop_music()
            elif event.key == pygame.K_n:
                next_music()
            elif event.key == pygame.K_b:
                previous_music()
            elif event.key == pygame.K_q:
                running = False

    screen.fill((30, 30, 30))

    title = font.render("Music Player", True, (255, 255, 255))
    track = font.render("Track: " + os.path.basename(playlist[current]), True, (0, 255, 0))
    keys = font.render("P-play S-stop N-next B-back Q-quit", True, (200, 200, 200))

    screen.blit(title, (250, 80))
    screen.blit(track, (180, 160))
    screen.blit(keys, (70, 240))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()