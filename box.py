import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pygame Example')

body = pygame.Surface((200, 200))
body.fill((255, 0, 0 ))

posi_x = random.randint(0, 800)
posi_y = random.randint(0, 600)
speed = 0.1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    
    if keys[pygame.K_UP]:
        posi_y = posi_y - min(speed, posi_y)
    if keys[pygame.K_DOWN]:
        posi_y = posi_y + min(speed, 600 - posi_y - 200)
    if keys[pygame.K_LEFT]:
        posi_x = posi_x - min(speed, posi_x)
    if keys[pygame.K_RIGHT]:
        posi_x = posi_x + min(speed, 800 - posi_x - 200)

    

    screen.fill((0, 0, 0))

    screen.blit(body, (posi_x, posi_y))

    pygame.display.flip()



