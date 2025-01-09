import pygame
from sys import exit
from random import randint

GAME_WIDTH = 1000
GAME_HEIGHT = 700
UNIT_SIZE = 20


def game_over():
    global game_active, score
    game_active = False
    score = player.sprite.score
    print(score)

    player.sprite.kill()
    player.add(Snake())

    food.sprite.kill()
    food.add(Apple())

def start_game():
    global game_active
    keys = pygame.key.get_pressed()
    if pygame.KEYDOWN:
        if not tracker:
            if keys[pygame.K_SPACE]:
                print('start')
                game_active = True
        else:
            if keys[pygame.K_r]:
                print('restart')
                game_active = True


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_coord = UNIT_SIZE
        self.y_coord = UNIT_SIZE
        self.degree = 90

        self.image = pygame.transform.rotozoom(pygame.image.load('Graphics/snake-svgrepo-com.png').convert_alpha(), self.degree, 0.15)
        self.rect = self.image.get_rect(topleft=(self.x_coord,self.y_coord))
        self.body_list = [self.rect]
        self.body_pos = [self.rect.topleft]

        self.body_segment = pygame.transform.rotozoom(pygame.image.load('Graphics/snake-body.png').convert_alpha(), self.degree, 0.15)
        self.eat_audio = pygame.mixer.Sound('Audio/food.mp3')
        self.eat_audio.set_volume(0.25)

        self.direction = 'right'
        self.speed = 0.2
        self.score = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.direction != 'down':  # Prevent 180-degree reverse movement
            self.direction = 'top'
            self.degree = 180
        elif keys[pygame.K_LEFT] and self.direction != 'right':
            self.direction = 'left'
            self.degree = 270
        elif keys[pygame.K_RIGHT] and self.direction != 'left':
            self.direction = 'right'
            self.degree = 90
        elif keys[pygame.K_DOWN] and self.direction != 'top':
            self.direction = 'down'
            self.degree = 0

        self.image = pygame.transform.rotozoom(pygame.image.load('Graphics/snake-svgrepo-com.png').convert_alpha(), self.degree, 0.15)

    def animate(self):
        # Update body segments to follow the one ahead
        for i in range(len(self.body_list) - 1, 0, -1):
            self.body_list[i].topleft = self.body_list[i - 1].topleft

        # Move the head
        if self.direction == 'left':
            self.body_list[0].x -= int(UNIT_SIZE+self.speed)
        elif self.direction == 'top':
            self.body_list[0].y -= int(UNIT_SIZE+self.speed)
        elif self.direction == 'right':
            self.body_list[0].x += int(UNIT_SIZE+self.speed)
        elif self.direction == 'down':
            self.body_list[0].y += int(UNIT_SIZE+self.speed)

        # Update the head rect for collisions
        self.rect = self.body_list[0]
        self.body_pos = []
        for segment in self.body_list:
            self.body_pos.append(segment.topleft)



    def check_food_collision(self):
        if pygame.sprite.spritecollide(player.sprite, food, False):
            # remove food instance and then reinitialize
            food.sprite.kill()
            self.eat_audio.play()
            food.add(Apple())

            self.speed += 0.05
            self.score+=1
            # Add a new body segment at the current tail position
            if self.body_list:
                tail_rect = self.body_list[-1]  # Get the last body segment
                new_segment = tail_rect.copy()
                self.body_list.append(new_segment)

    def wall_collision(self):
        if self.rect.left < 0 or self.rect.right > GAME_WIDTH or self.rect.top < 0 or self.rect.bottom > GAME_HEIGHT:
            game_over()

    def self_collision(self):
        if self.rect.topleft in self.body_pos[10:]:
            print('Self collision')
            game_over()

    def draw(self, surface):
        # Draw the body
        for segment in self.body_list[1:]:
            surface.blit(self.body_segment, segment)

        # Draw the head
        surface.blit(self.image, self.body_list[0].topleft)

    def update(self):
        self.player_input()
        self.animate()
        self.check_food_collision()
        self.wall_collision()
        self.self_collision()

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = randint(5,45)
        self.y = randint(5,30)
        self.image = pygame.transform.rotozoom(pygame.image.load('Graphics/apple-svgrepo-com.png').convert_alpha(), 0, 0.2)
        self.rect = self.image.get_rect(topleft=(self.x*UNIT_SIZE, self.y*UNIT_SIZE))



pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Snake Game')

player = pygame.sprite.GroupSingle()
player.add(Snake())

food = pygame.sprite.GroupSingle()
food.add(Apple())

background = pygame.image.load('Graphics/background.jpg').convert_alpha()
background = pygame.transform.rotozoom(background, 0, 3)
background_rect = background.get_rect(topleft=(0,0))

Bg_Music = pygame.mixer.Sound('Audio/bg-music.wav')
Bg_Music.play(loops=-1)

game_active = False
tracker = False #tracks if code already run to distinguish between game-over screen and start game screen f this nig
clock = pygame.time.Clock()
score = 0

while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, background_rect)

    if game_active:
        player.sprite.draw(screen)
        player.update()

        food.draw(screen)
        Bg_Music.set_volume(0.05)
        tracker = True
    else:
        Bg_Music.set_volume(0.15)

        if not tracker:
            title_font = pygame.font.Font('font/Tiny5-Regular.ttf', 150)
            title_text = title_font.render('Snake Pixel', False, '#1B4332')
            title_rect = title_text.get_rect(midbottom=(GAME_WIDTH/2, GAME_HEIGHT/3))
            screen.blit(title_text, title_rect)

            snake_icon = pygame.transform.rotozoom(pygame.image.load('Graphics/snake-svgrepo-com.png').convert_alpha(), 0, 0.5)
            icon_rect = snake_icon.get_rect(midtop=(GAME_WIDTH/2, title_rect.bottom+25))
            screen.blit(snake_icon, icon_rect)

            instruction_font = pygame.font.Font('font/Tiny5-Regular.ttf', 60)
            instruction_text = instruction_font.render('Press Space to start.', False, (255, 0, 0))
            instruction_rect = instruction_text.get_rect(midbottom=(GAME_WIDTH/2, GAME_HEIGHT*0.8))
            screen.blit(instruction_text, instruction_rect)

            start_game()#check input for start
        else: #game-over
            title_font = pygame.font.Font('font/Tiny5-Regular.ttf', 150)
            title_text = title_font.render('Game Over', False, '#990F02')
            title_rect = title_text.get_rect(midbottom=(GAME_WIDTH / 2, GAME_HEIGHT / 3))
            screen.blit(title_text, title_rect)

            snake_icon = pygame.transform.rotozoom(pygame.image.load('Graphics/snake-svgrepo-com.png').convert_alpha(),
                                                   0, 0.5)
            icon_rect = snake_icon.get_rect(midtop=(GAME_WIDTH / 2, title_rect.bottom + 25))
            screen.blit(snake_icon, icon_rect)

            instruction_font = pygame.font.Font('font/Tiny5-Regular.ttf', 60)
            instruction_text = instruction_font.render('Press \'r\' to restart.', False, (255, 0, 0))
            instruction_rect = instruction_text.get_rect(midbottom=(GAME_WIDTH / 2, GAME_HEIGHT * 0.75))
            screen.blit(instruction_text, instruction_rect)


            score_font = pygame.font.Font('font/Pixeltype.ttf', 60)
            score_text = score_font.render(f'Score: {score}', False, (255, 0, 0))
            score_rect = score_text.get_rect(midtop=(GAME_WIDTH / 2, instruction_rect.bottom+25))
            screen.blit(score_text, score_rect)

            start_game()

    pygame.display.update()
    clock.tick(20)