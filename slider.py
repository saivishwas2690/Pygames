import pygame, asyncio
import sys
import random
import math

pygame.init()

score = 0

def slider_bounce(slider, ball):
    global score
    distance = abs(ball.center()[1] - slider.y)
    if distance <= ball.radius and ball.x + ball.radius >= slider.x and ball.x + ball.radius <= slider.x + slider.width:
        ball.vertical_speed = -abs(ball.vertical_speed)
        ball.horizontal_speed = ball.horizontal_speed + random.uniform(-0.3, 0.3)
        score += 1


class Slider(pygame.Surface):
    def __init__(self, x, y, width, height, color):
        super().__init__((width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        pygame.draw.rect(self, color, (0, 0, width, height))

    def update(self, score):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x = max(0, self.x - 0.7)
        if keys[pygame.K_RIGHT]:
            self.x = min(800 - self.width, self.x + 0.7)
        self.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), True, (0, 0, 0))
        self.blit(text, (0, 0))

def gameover(ball):
    if ball.y >= 600 - 2*ball.radius:
        return True
    return False

class ScoreBoard(pygame.Surface):
    def __init__(self, x, y, width, height, color):
        super().__init__((width, height), pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    

    def update(self, score):
        self.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), True, (255, 255, 255))
        self.blit(text, (0, 0))

class Ball(pygame.Surface):
    def __init__(self, x, y, horizontal_speed, vertical_speed, radius, color, mass):
        super().__init__((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.radius = radius
        self.horizontal_speed = horizontal_speed
        self.vertical_speed = vertical_speed
        self.color = color
        self.mass = mass
        pygame.draw.circle(self, color, (radius, radius), radius)

    def center(self):
        return (self.x + self.radius, self.y + self.radius)
    
    def bounce(self):
        if(self.y <= 0):
            self.vertical_speed = -self.vertical_speed
            
        if(self.x <= 0 or self.x >= 800 - 2*self.radius):
            self.horizontal_speed = -self.horizontal_speed
            
    def update(self):
        self.x = min(800 - 2*self.radius, max(0, self.x + self.horizontal_speed))
        self.y = max(0, self.y + self.vertical_speed)


    @staticmethod
    def collisioncheck(ball1, ball2):
        dx = ball2.center()[0] - ball1.center()[0]
        dy = ball2.center()[1] - ball1.center()[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= ball1.radius + ball2.radius:
            m1 = ball1.mass
            m2 = ball2.mass
            
            nx = dx / distance
            ny = dy / distance

            v1_parallel = ball1.horizontal_speed * nx + ball1.vertical_speed * ny
            v1_perp = -ball1.horizontal_speed * ny + ball1.vertical_speed * nx
            v2_parallel = ball2.horizontal_speed * nx + ball2.vertical_speed * ny
            v2_perp = -ball2.horizontal_speed * ny + ball2.vertical_speed * nx

            v1_parallel_new = (v1_parallel * (m1 - m2) + 2 * m2 * v2_parallel) / (m1 + m2)
            v2_parallel_new = (v2_parallel * (m2 - m1) + 2 * m1 * v1_parallel) / (m1 + m2)

            v1_perp_new = v1_perp
            v2_perp_new = v2_perp

            ball1.horizontal_speed = v1_parallel_new * nx - v1_perp_new * ny
            ball1.vertical_speed = v1_parallel_new * ny + v1_perp_new * nx
            ball2.horizontal_speed = v2_parallel_new * nx - v2_perp_new * ny
            ball2.vertical_speed = v2_parallel_new * ny + v2_perp_new * nx

    def applygravity(self, gravity):
        self.vertical_speed += gravity
    

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pygame Example')

posi_x = random.randint(0, 600)
posi_y = random.randint(0, 400)

horizontal_speed = 0.1
vertical_speed = 0.1

gravity = 0.001

ball1 = Ball(random.randint(0, 600), 0, horizontal_speed=horizontal_speed, vertical_speed=vertical_speed, radius=50, color=(255, 0, 0), mass=2)
ball2 = Ball(random.randint(0, 600), random.randint(0, 400), horizontal_speed=2*horizontal_speed, vertical_speed=2*vertical_speed, radius=50, color=(0, 255, 0), mass=1)
ball3 = Ball(random.randint(0, 600), random.randint(0, 400), horizontal_speed=3*horizontal_speed, vertical_speed=3*vertical_speed, radius=50, color=(0, 0, 255), mass=3)


slider1 = Slider(0, 600-20, 200, 20, (255, 255, 255))


async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if gameover(ball1):
            pygame.Surface((800, 600)).fill((0, 0, 0))
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over, Score: " + str(score), True, (255, 255, 255))
            screen.blit(text, (300, 300))
            pygame.display.flip()
            await asyncio.sleep(5)
            pygame.quit()
            sys.exit()


        slider1.update(score)
        slider_bounce(slider1, ball1)

        ball1.update()

        ball1.bounce()

        screen.fill((0, 0, 0))
        screen.blit(ball1, (ball1.x, ball1.y))
        screen.blit(slider1, (slider1.x, slider1.y))

        ball1.applygravity(gravity)

        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())