import pygame
import random

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)
coin_sound = pygame.mixer.Sound("assets/coin.wav")

background = pygame.image.load("assets/background.png").convert()
player_img = pygame.image.load("assets/player.png").convert_alpha()
player_rect = player_img.get_rect(center=(400, 300))
speed = 4

coin_img = pygame.image.load("assets/coin.png").convert_alpha()
coin_rect = coin_img.get_rect(center=(400, -20))
coin_speed = 5

score = 0
font = pygame.font.Font(None, 36)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > 800:
        player_rect.right = 800
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > 600:
        player_rect.bottom = 600

    coin_rect.y += coin_speed

    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_rect.center = (random.randint(20, 780), -20)

    if coin_rect.top > 600:
        coin_rect.center = (random.randint(20, 780), -20)

    screen.blit(background, (0, 0))
    screen.blit(coin_img, coin_rect)
    screen.blit(player_img, player_rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
