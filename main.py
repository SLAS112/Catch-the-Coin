import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

player_img = pygame.image.load("assets/player.png").convert_alpha()
player_rect = player_img.get_rect(center=(400, 300))

running = True
speed = 4

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

    

    screen.fill((70, 70, 70))
    screen.blit(player_img, player_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()