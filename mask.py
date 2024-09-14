import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Collision Detection Example')

# Create two surfaces with transparency
surface1 = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.circle(surface1, (255, 0, 0), (50, 50), 50)

surface2 = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.circle(surface2, (0, 255, 0), (50, 50), 50)

# Create masks from the surfaces
mask1 = pygame.mask.from_surface(surface1)
mask2 = pygame.mask.from_surface(surface2)

# Position of the surfaces
pos1 = pygame.Rect(200, 200, 100, 100)
pos2 = pygame.Rect(250, 250, 100, 100)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Blit the surfaces onto the screen
    screen.blit(surface1, pos1.topleft)
    screen.blit(surface2, pos2.topleft)

    # Check for collision
    offset = (pos2.left - pos1.left, pos2.top - pos1.top)
    if mask1.overlap(mask2, offset):
        print("Collision detected!")

    # Update the display
    pygame.display.flip()
