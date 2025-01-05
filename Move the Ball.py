
import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global SCREEN_HEIGHT, SCREEN_WIDTH
        # always start at center
        self.x_coords = SCREEN_WIDTH // 2
        self.y_coords = SCREEN_HEIGHT// 2
        self.rad = 50
        # 0 - left
        # 1 - up
        # 2 - right
        # 3 - down
        self.direction = 0
        self.speed = 240


    def player_input(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.direction = 1
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.direction = 2
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.direction = 3
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.direction = 0

    def animate_player(self, dt):
        if self.direction == 0:
            self.x_coords-= self.speed * dt
        if self.direction == 1:
            self.y_coords-= self.speed * dt
        if self.direction == 2:
            self.x_coords += self.speed * dt
        if self.direction == 3:
            self.y_coords += self.speed * dt
        pygame.draw.circle(screen, 'red', (self.x_coords, self.y_coords), self.rad)

    def check_overbound(self):
        global SCREEN_HEIGHT, SCREEN_WIDTH
        if self.x_coords > SCREEN_WIDTH + 50:
            self.x_coords = 0
        if self.x_coords < -50:
            self.x_coords = SCREEN_WIDTH + 50

        if self.y_coords > SCREEN_HEIGHT + 50:
            self.y_coords = 0
        if self.y_coords < -50:
            self.y_coords = SCREEN_HEIGHT + 50


    def update(self, dt):
        self.player_input()
        self.animate_player(dt)
        self.check_overbound()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ball Move')

player = pygame.sprite.GroupSingle()
player.add(Player())

clock = pygame.time.Clock()
dt = 1


while True:
    dt = clock.tick(60) / 1000
    print(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    screen.fill((0,0,0))
    player.update(dt)

    pygame.display.update()