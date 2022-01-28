import pygame

import os

import random

pygame.font.init()

# GAME WINDOW PARAMETERS

DISPLAY = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Batman vs Joker")

# CHARACTER
character_width = 70

character_height = 70

character_speed = 7

character_image = pygame.image.load(os.path.join("Assets_TestGame", "character2.png"))

character = pygame.transform.scale(character_image, (character_width, character_height))

# GAME OBJECTS

enemy_image = pygame.image.load(os.path.join("Assets_TestGame", "joker2.png"))

enemy_image = pygame.transform.scale(enemy_image, (80, 80))

game_background_image = pygame.image.load(os.path.join("Assets_TestGame", "background1.jpg"))

character_weapon = pygame.image.load(os.path.join("Assets_TestGame", "batarang.png"))

batarang = pygame.transform.scale(character_weapon, (5, 5))

MAX_Batarangs = 3

# COLORS and FONTS

GAME_OVER_FONT = pygame.font.SysFont("verdanaproblack", 100)

HEALTH_FONT = pygame.font.SysFont("verdanaproblack", 40)

TITLE_FONT = pygame.font.SysFont("verdanaproblack", 60)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# EVENTS

enemy_hit = pygame.USEREVENT

joker_shoots = pygame.USEREVENT + 1

player_damage = pygame.USEREVENT + 2


def game_window(character_position, number_of_batarangs, enemy_position, joker_health,
                number_of_joker_projectiles, player_health):
    title_text = TITLE_FONT.render("STOP THE JOKER!", True, WHITE)

    joker_health_text = HEALTH_FONT.render("Joker's Health: " + str(joker_health), True, RED)

    player_health_text = HEALTH_FONT.render("Batman's Health: " + str(player_health), True, RED)

    DISPLAY.fill(BLACK)

    DISPLAY.blit(game_background_image, (0, 130))

    DISPLAY.blit(title_text, (220, 20))

    DISPLAY.blit(joker_health_text, (475, 95))

    DISPLAY.blit(player_health_text, (80, 95))

    DISPLAY.blit(character, (character_position.x, character_position.y))

    DISPLAY.blit(enemy_image, (enemy_position.x, enemy_position.y))

    for joker_projectile in number_of_joker_projectiles:
        pygame.draw.rect(DISPLAY, RED, joker_projectile)

    for batarang_position in number_of_batarangs:
        pygame.draw.rect(DISPLAY, BLACK, batarang_position)

    pygame.display.update()


def character_movement(user_key_pressed, character_position):
    if user_key_pressed[pygame.K_UP] and character_position.y > 135:
        character_position.y -= character_speed
    if user_key_pressed[pygame.K_DOWN] and character_position.y < 620:
        character_position.y += character_speed
    if user_key_pressed[pygame.K_RIGHT] and character_position.x < 720:
        character_position.x += character_speed
    if user_key_pressed[pygame.K_LEFT] and character_position.x > 0:
        character_position.x -= character_speed


def batarang_movement(number_of_batarangs, enemy_position):
    for batarang_position in number_of_batarangs:
        batarang_position.x += 10
        if enemy_position.colliderect(batarang_position):
            pygame.event.post(pygame.event.Event(enemy_hit))
            pygame.event.post(pygame.event.Event(joker_shoots))
            number_of_batarangs.remove(batarang_position)
            enemy_position.x = random.randint(500, 650)
            enemy_position.y = random.randint(140, 500)
        elif batarang_position.x > 750:
            number_of_batarangs.remove(batarang_position)


def collisions():
    pass


def joker_combat(number_of_joker_projectiles, character_position):
    for joker_projectile in number_of_joker_projectiles:
        joker_projectile.x -= 12
        if character_position.colliderect(joker_projectile):
            pygame.event.post(pygame.event.Event(player_damage))
            number_of_joker_projectiles.remove(joker_projectile)


def main():

    player_death_message = GAME_OVER_FONT.render("You Died!", True, BLACK)

    game_over_message = GAME_OVER_FONT.render("You Killed The Joker!", True, BLACK)

    character_position = pygame.Rect(100, 350, character_width, character_height)

    enemy_position = pygame.Rect(550, 350, character_width, character_height)

    joker_health = 10

    player_health = 3

    clock = pygame.time.Clock()

    number_of_batarangs = []

    number_of_joker_projectiles = []

    run_game = True
    while run_game:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(number_of_batarangs) < MAX_Batarangs:
                    batarang_position = pygame.Rect(int(character_position.x) + 50, character_position.y + 40, 20, 10)
                    number_of_batarangs.append(batarang_position)

            if event.type == enemy_hit:
                joker_health -= 1
                joker_projectile = pygame.Rect(int(enemy_position.x), int(enemy_position.y) + 40, 20, 10)
                number_of_joker_projectiles.append(joker_projectile)

            if event.type == player_damage:
                player_health -= 1

        if joker_health <= 0:
            DISPLAY.blit(game_over_message, (50, 350))
            pygame.display.update()
            pygame.time.delay(5000)
            break
        elif player_health <= 0:
            DISPLAY.blit(player_death_message, (240, 350))
            pygame.display.update()
            pygame.time.delay(5000)
            break

        user_key_pressed = pygame.key.get_pressed()

        joker_combat(number_of_joker_projectiles, character_position)

        collisions()

        character_movement(user_key_pressed, character_position)

        batarang_movement(number_of_batarangs, enemy_position)

        game_window(character_position, number_of_batarangs, enemy_position, joker_health, number_of_joker_projectiles,
                    player_health)

    main()


if __name__ == "__main__":
    main()
