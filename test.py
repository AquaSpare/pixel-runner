import math
import random
from enum import Enum
from random import randint, choice
from typing import Any

import pygame
from sys import exit


class ObstacleType(Enum):
    SNAIL = 0
    FLY = 1


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()

        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.gravity = 0

        self.image = self.player_walk[0]
        self.rect = self.image.get_rect(midbottom=(80, 300))

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animate_states(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            self.image = self.player_walk[int(self.player_index) % 2]

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.player_input()
        self.apply_gravity()
        self.animate_states()

    def reset(self):
        self.rect.midbottom = (80, 300)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle: ObstacleType):
        super().__init__()

        if obstacle == ObstacleType.FLY:
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
            self.speed = 0.1

        elif obstacle == ObstacleType.SNAIL:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
            self.speed = 0.1
        else:
            raise ValueError('No valid obstacle type given')

        self.animation_index = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += self.speed
        self.image = self.frames[int(self.animation_index) % 2]

    def move(self):
        self.rect.x -= 6

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.animation_state()
        self.move()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = math.floor((pygame.time.get_ticks() - start_time) / 1000) + 1
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = None
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5)
bg_music.play(loops=-1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name_surf = test_font.render('Valters pixel runner', False, (111, 196, 169))
game_name_rect = game_name_surf.get_rect(center=(200, 80))

game_message_surf = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message_surf.get_rect(center=(200, 340))

vallman = pygame.image.load('graphics/misc/VALPIX.png').convert_alpha()
vallman_rect = vallman.get_rect(bottomright=(800, 400))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choices(list(ObstacleType), weights=(10, 5), k=1)[0]))

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, sky_surface.get_height()))

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        obstacles_rect_list = []
        player_gravity = 0

        screen.fill((94, 129, 162))
        screen.blit(vallman, vallman_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(200, 340))

        if score is None:
            screen.blit(game_message_surf, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

        screen.blit(game_name_surf, game_name_rect)

    pygame.display.update()
    clock.tick(60)
