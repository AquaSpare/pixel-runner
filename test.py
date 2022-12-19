import math
from random import randint, choice

import pygame
from sys import exit


def display_score():
    current_time = math.floor((pygame.time.get_ticks() - start_time) / 1000) + 1
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list: list[pygame.rect.Rect]):
    for obstacle_rect in obstacle_list:
        obstacle_rect.x += -5

        if obstacle_rect.bottom == 300:
            screen.blit(snail_surf, obstacle_rect)
        else:
            screen.blit(fly_surf, obstacle_rect)

    obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.right > -50]
    return obstacle_list


def collisions(player: pygame.rect.Rect, obstacle_list: list[pygame.rect.Rect]) -> bool:
    for obstacle in obstacle_list:
        if player.colliderect(obstacle):
            return False
    return True


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        player_surf = player_walk[int(player_index) % 2]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0

score = None

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacles_rect_list = []

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 1300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
                    print(player_rect.bottomleft)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == obstacle_timer:
                if choice([True, False]):
                    obstacles_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacles_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

            if event.type == snail_animation_timer:
                snail_frame_index = not snail_frame_index
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                fly_frame_index = not fly_frame_index
                fly_surf = fly_frames[fly_frame_index]


        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, sky_surface.get_height()))

        score = display_score()

        # PLAYER
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacles_rect_list = obstacle_movement(obstacles_rect_list)

        # collision
        game_active = collisions(player_rect, obstacles_rect_list)

    else:
        obstacles_rect_list = []
        player_rect.midbottom = (80, 300)
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
