import pygame, sys
from pygame.locals import *
import random, time
 
# Initializing pygame
pygame.init()
 
# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
MON = 0

# Enemy speed increases after every N collected coins
N = 5
last_speed_level = 0
 
# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("raceimages/AnimatedStreet.png")
 
# Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("raceimages/Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)  

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)

        # If enemy leaves the screen, move it back to the top
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)
 
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 

        # Load original coin image once
        self.original_image = pygame.image.load("raceimages/Coin.png")
        self.reset_coin()

    def reset_coin(self):
        # Random coin weight: 1, 2 or 3
        self.weight = random.randint(1, 3)

        # Different weight coins have different sizes
        if self.weight == 1:
            size = 30
        elif self.weight == 2:
            size = 40
        else:
            size = 50

        self.image = pygame.transform.scale(self.original_image, (size, size))
        self.rect = self.image.get_rect()

        # Random position on the road
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -30)

    def move(self):
        self.rect.move_ip(0, 8)

        # If coin leaves the screen, generate a new random coin
        if (self.rect.top > 600):
            self.reset_coin()



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("raceimages/Player.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[pygame.K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[pygame.K_RIGHT]:
                  self.rect.move_ip(5, 0)
                   
# Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()
 
# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1) 
 
# Game Loop
while True:
       
    # Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))

    # Display score
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    # Display collected coins
    scorescoin = font_small.render(str(MON), True, BLACK)
    coinrect = scorescoin.get_rect(topright = (SCREEN_WIDTH-10,10))
    DISPLAYSURF.blit(scorescoin, coinrect)

    # Moves and re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Check if player collected a coin
    collectedcoin = pygame.sprite.spritecollideany(P1, coins)

    if collectedcoin:    
        # Add coin weight to total coins
        MON += collectedcoin.weight

        # Generate a new coin after collecting
        collectedcoin.reset_coin()

        # Increase enemy speed every N collected coins
        speed_level = MON // N

        if speed_level > last_speed_level:
            SPEED += 1
            last_speed_level = speed_level

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()

          for entity in all_sprites:
                entity.kill()

          time.sleep(2)
          pygame.quit()
          sys.exit()        
         
    pygame.display.update()
    FramePerSec.tick(FPS)