import pygame
import random
import time
import os

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

background = pygame.image.load("assets/background.png").convert()
player_skins = [
    pygame.image.load("assets/player.png").convert_alpha(),
    pygame.image.load("assets/player2.png").convert_alpha()
]
current_skin = 0

coin_img = pygame.image.load("assets/coin.png").convert_alpha()
spike_img = pygame.image.load("assets/spike.png").convert_alpha()
potion_img = pygame.image.load("assets/potion.png").convert_alpha()

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 120)

if not os.path.exists("record.txt"):
    with open("record.txt", "w") as f:
        f.write("0")

def load_record():
    with open("record.txt", "r") as f:
        return int(f.read().strip())

def save_record(new_record):
    with open("record.txt", "w") as f:
        f.write(str(new_record))

def game_loop():
    global current_skin
    player_img = player_skins[current_skin]
    player_rect = player_img.get_rect(center=(400, 520))
    speed = 7
    coin_rect = coin_img.get_rect(center=(400, -20))
    coin_speed = 7
    spikes = []
    spike_speed = 7
    spawn_interval = 2000
    last_spawn_time = pygame.time.get_ticks()
    start_time = time.time()
    potion_rect = potion_img.get_rect(center=(random.randint(20, 780), -20))
    potion_speed = 7
    potion_active = False
    potion_start_time = 0
    last_poison_tick = 0
    max_hp = 100
    hp = 100
    max_shield = 100
    shield = 100
    score = 0
    damage = 20

    def reset_coin():
        coin_rect.center = (random.randint(20, 780), -20)

    def spawn_spike():
        rect = spike_img.get_rect(center=(random.randint(20, 780), -20))
        spikes.append(rect)

    def reset_potion():
        potion_rect.center = (random.randint(20, 780), -20)

    def game_over_animation():
        dark = pygame.Surface((800, 600))
        dark.fill((0, 0, 0))
        for alpha in range(0, 180, 5):
            dark.set_alpha(alpha)
            screen.blit(dark, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)
        text = big_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (150, 250))
        pygame.display.flip()
        time.sleep(2)

    def pause_menu():
        global current_skin
        resume_btn = pygame.Rect(300, 200, 200, 60)
        skins_btn = pygame.Rect(300, 270, 200, 60)
        records_btn = pygame.Rect(300, 340, 200, 60)
        main_menu_btn = pygame.Rect(300, 410, 200, 60)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_btn.collidepoint(event.pos):
                        return
                    elif skins_btn.collidepoint(event.pos):
                        skins_menu()
                    elif records_btn.collidepoint(event.pos):
                        records_screen()
                    elif main_menu_btn.collidepoint(event.pos):
                        raise Exception("MAIN_MENU")

            screen.fill((50, 50, 50))
            pygame.draw.rect(screen, (50, 150, 50), resume_btn)
            screen.blit(font.render("Продолжить", True, (255, 255, 255)), (resume_btn.x + 35, resume_btn.y + 15))
            pygame.draw.rect(screen, (50, 50, 150), skins_btn)
            screen.blit(font.render("Скины", True, (255, 255, 255)), (skins_btn.x + 60, skins_btn.y + 15))
            pygame.draw.rect(screen, (150, 50, 50), records_btn)
            screen.blit(font.render("Рекорды", True, (255, 255, 255)), (records_btn.x + 45, records_btn.y + 15))
            pygame.draw.rect(screen, (150, 150, 50), main_menu_btn)
            screen.blit(font.render("В меню", True, (255, 255, 255)), (main_menu_btn.x + 55, main_menu_btn.y + 15))
            pygame.display.flip()
            clock.tick(60)

    def skins_menu():
        global current_skin
        back_btn = pygame.Rect(300, 450, 200, 60)
        skin1_btn = pygame.Rect(200, 250, 150, 60)
        skin2_btn = pygame.Rect(450, 250, 150, 60)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.collidepoint(event.pos):
                        return
                    elif skin1_btn.collidepoint(event.pos):
                        current_skin = 0
                        return
                    elif skin2_btn.collidepoint(event.pos):
                        current_skin = 1
                        return
            screen.fill((30, 30, 30))
            pygame.draw.rect(screen, (150, 50, 50), back_btn)
            screen.blit(font.render("Назад", True, (255, 255, 255)), (back_btn.x + 55, back_btn.y + 15))
            pygame.draw.rect(screen, (50, 150, 50), skin1_btn)
            screen.blit(font.render("Скин 1", True, (255, 255, 255)), (skin1_btn.x + 35, skin1_btn.y + 15))
            pygame.draw.rect(screen, (50, 150, 50), skin2_btn)
            screen.blit(font.render("Скин 2", True, (255, 255, 255)), (skin2_btn.x + 35, skin2_btn.y + 15))
            pygame.display.flip()
            clock.tick(60)

    running = True
    dead = False

    while running:
        if hp <= 0 and not dead:
            dead = True
            game_over_animation()
            record = load_record()
            if score > record:
                save_record(score)
            return

        now = pygame.time.get_ticks()
        if time.time() - start_time >= 30:
            start_time = time.time()
            spawn_interval = max(300, spawn_interval - 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    try:
                        pause_menu()
                    except Exception as e:
                        if str(e) == "MAIN_MENU":
                            return

        keys = pygame.key.get_pressed()
        current_speed = speed * (0.7 if potion_active else 1.0)

        if keys[pygame.K_LEFT]:
            player_rect.x -= current_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += current_speed
        if keys[pygame.K_UP]:
            player_rect.y -= current_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += current_speed

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
            if hp < max_hp:
                hp += 10
                if hp > max_hp:
                    hp = max_hp
            coin_rect.center = (random.randint(20, 780), -20)
        if coin_rect.top > 600:
            coin_rect.center = (random.randint(20, 780), -20)

        if now - last_spawn_time > spawn_interval:
            rect = spike_img.get_rect(center=(random.randint(20, 780), -20))
            spikes.append(rect)
            last_spawn_time = now

        for spike in spikes[:]:
            spike.y += spike_speed
            if player_rect.colliderect(spike):
                if shield > 0:
                    shield -= damage
                    if shield < 0:
                        shield = 0
                else:
                    hp -= damage
                    if hp < 0:
                        hp = 0
                spikes.remove(spike)
            elif spike.top > 600:
                spikes.remove(spike)

        potion_rect.y += potion_speed
        if player_rect.colliderect(potion_rect):
            potion_active = True
            potion_start_time = time.time()
            last_poison_tick = time.time()
            potion_rect.center = (random.randint(20, 780), -20)
        if potion_rect.top > 600:
            potion_rect.center = (random.randint(20, 780), -20)

        if potion_active:
            if time.time() - last_poison_tick >= 1:
                last_poison_tick = time.time()
                if shield > 0:
                    shield -= 5
                    if shield < 0:
                        shield = 0
                else:
                    hp -= 5
                    if hp < 0:
                        hp = 0
            if time.time() - potion_start_time >= 5:
                potion_active = False

        screen.blit(background, (0, 0))
        screen.blit(coin_img, coin_rect)
        screen.blit(potion_img, potion_rect)
        for spike in spikes:
            screen.blit(spike_img, spike)
        screen.blit(player_skins[current_skin], player_rect)

        pygame.draw.rect(screen, (0, 0, 255), (10, 50, 200 * (shield / max_shield), 15))
        pygame.draw.rect(screen, (255, 255, 255), (10, 50, 200, 15), 2)
        pygame.draw.rect(screen, (255, 0, 0), (10, 70, 200 * (hp / max_hp), 15))
        pygame.draw.rect(screen, (255, 255, 255), (10, 70, 200, 15), 2)

        screen.blit(font.render(f"Score: {score}", True, (255, 255, 0)), (10, 10))
        screen.blit(font.render(f"HP: {hp}", True, (255, 50, 50)), (220, 70))
        screen.blit(font.render(f"Shield: {shield}", True, (100, 150, 255)), (220, 50))
        if potion_active:
            screen.blit(font.render("POISONED", True, (100, 255, 100)), (350, 10))

        pygame.display.flip()
        clock.tick(60)

def records_screen():
    back_button = pygame.Rect(300, 450, 200, 60)
    record = load_record()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
        screen.fill((0, 0, 0))
        screen.blit(big_font.render("Рекорды", True, (255, 255, 255)), (200, 100))
        screen.blit(font.render(f"Лучший счёт: {record}", True, (255, 255, 0)), (270, 300))
        pygame.draw.rect(screen, (150, 50, 50), back_button)
        screen.blit(font.render("Назад", True, (255, 255, 255)), (back_button.x + 55, back_button.y + 15))
        pygame.display.flip()
        clock.tick(60)

def menu_screen():
    start_button = pygame.Rect(300, 300, 200, 60)
    records_button = pygame.Rect(300, 380, 200, 60)
    skins_button = pygame.Rect(300, 460, 200, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "start"
                if records_button.collidepoint(event.pos):
                    return "records"
                if skins_button.collidepoint(event.pos):
                    return "skins"

        screen.fill((0, 0, 0))
        screen.blit(big_font.render("My Game", True, (255, 255, 255)), (200, 120))
        pygame.draw.rect(screen, (50, 150, 50), start_button)
        screen.blit(font.render("НАЧАТЬ", True, (255, 255, 255)), (start_button.x + 50, start_button.y + 15))
        pygame.draw.rect(screen, (50, 50, 150), records_button)
        screen.blit(font.render("РЕКОРДЫ", True, (255, 255, 255)), (records_button.x + 35, records_button.y + 15))
        pygame.draw.rect(screen, (150, 50, 150), skins_button)
        screen.blit(font.render("СКИНЫ", True, (255, 255, 255)), (skins_button.x + 55, skins_button.y + 15))
        pygame.display.flip()
        clock.tick(60)

while True:
    choice = menu_screen()
    if choice == "start":
        game_loop()
    elif choice == "records":
        records_screen()
    elif choice == "skins":
        def skins_menu_main():
            global current_skin
            back_btn = pygame.Rect(300, 450, 200, 60)
            skin1_btn = pygame.Rect(200, 250, 150, 60)
            skin2_btn = pygame.Rect(450, 250, 150, 60)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if back_btn.collidepoint(event.pos):
                            return
                        elif skin1_btn.collidepoint(event.pos):
                            current_skin = 0
                        elif skin2_btn.collidepoint(event.pos):
                            current_skin = 1
                screen.fill((30, 30, 30))
                pygame.draw.rect(screen, (150, 50, 50), back_btn)
                screen.blit(font.render("Назад", True, (255, 255, 255)), (back_btn.x + 55, back_btn.y + 15))
                pygame.draw.rect(screen, (50, 150, 50), skin1_btn)
                screen.blit(font.render("Скин 1", True, (255, 255, 255)), (skin1_btn.x + 35, skin1_btn.y + 15))
                pygame.draw.rect(screen, (50, 150, 50), skin2_btn)
                screen.blit(font.render("Скин 2", True, (255, 255, 255)), (skin2_btn.x + 35, skin2_btn.y + 15))
                pygame.display.flip()
                clock.tick(60)
        skins_menu_main()
