import pygame
import random
import time
import os
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

player_skins = [
    pygame.image.load("assets/player.png").convert_alpha(),
    pygame.image.load("assets/player2.png").convert_alpha()
]
current_skin = 0
difficulty = "normal"

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

class Player:
    def __init__(self):
        self.image = player_skins[current_skin]
        self.rect = self.image.get_rect(center=(400, 520))
        self.speed = 9
        self.max_hp = 100
        self.hp = 100
        self.max_shield = 100
        self.shield = 100

    def move(self, keys):
        current_speed = self.speed
        if keys[pygame.K_LSHIFT]:
            current_speed *= 1.5
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += current_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= current_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += current_speed
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, 800)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, 600)

    def draw(self, screen):
        screen.blit(player_skins[current_skin], self.rect)

class Coin:
    def __init__(self):
        self.image = coin_img
        self.rect = self.image.get_rect(center=(random.randint(20, 780), -20))
        self.speed = 7

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.rect.center = (random.randint(20, 780), -20)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Spike:
    def __init__(self, speed):
        self.image = spike_img
        self.rect = self.image.get_rect(center=(random.randint(20, 780), -20))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Potion:
    def __init__(self):
        self.image = potion_img
        self.rect = self.image.get_rect(center=(random.randint(20, 780), -20))
        self.speed = 7
        self.active = False
        self.start_time = 0
        self.last_tick = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.rect.center = (random.randint(20, 780), -20)

    def activate(self):
        self.active = True
        self.start_time = time.time()
        self.last_tick = time.time()
        self.rect.center = (random.randint(20, 780), -20)

    def check(self, player):
        if self.active:
            if time.time() - self.last_tick >= 1:
                self.last_tick = time.time()
                if player.shield > 0:
                    player.shield -= 5
                    if player.shield < 0:
                        player.shield = 0
                else:
                    player.hp -= 5
                    if player.hp < 0:
                        player.hp = 0
            if time.time() - self.start_time >= 5:
                self.active = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.active:
            screen.blit(font.render("POISONED", True, (100, 255, 100)), (350, 10))

class Game:
    def __init__(self):
        self.player = Player()
        self.coin = Coin()
        self.spikes = []
        self.potion = Potion()
        self.score = 0
        self.damage = 20
        self.spawn_interval = 2000
        self.last_spawn_time = pygame.time.get_ticks()
        self.start_time = time.time()
        self.dead = False
        self.apply_difficulty()
        self.load_background()

    def apply_difficulty(self):
        global difficulty
        if difficulty == "easy":
            self.damage = 10
            self.spawn_interval = 2500
            self.spike_speed = 5
            self.coin.speed = 6
        elif difficulty == "normal":
            self.damage = 20
            self.spawn_interval = 2000
            self.spike_speed = 7
            self.coin.speed = 7
        elif difficulty == "hard":
            self.damage = 30
            self.spawn_interval = 1400
            self.spike_speed = 10
            self.coin.speed = 8

    def load_background(self):
        global difficulty
        if difficulty == "easy":
            self.background = pygame.image.load("assets/background_easy.png").convert()
        elif difficulty == "normal":
            self.background = pygame.image.load("assets/background_normal.png").convert()
        elif difficulty == "hard":
            self.background = pygame.image.load("assets/background_hard.png").convert()

    def spawn_spike(self):
        self.spikes.append(Spike(self.spike_speed))
        self.last_spawn_time = pygame.time.get_ticks()

    def game_over(self):
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
        record = load_record()
        if self.score > record:
            save_record(self.score)

    def pause_menu(self):
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
                        self.skins_menu()
                    elif records_btn.collidepoint(event.pos):
                        self.records_screen()
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

    def skins_menu(self):
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
                        self.player.image = player_skins[current_skin]
                        return
                    elif skin2_btn.collidepoint(event.pos):
                        current_skin = 1
                        self.player.image = player_skins[current_skin]
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

    def records_screen(self):
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

    def run(self):
        running = True
        while running:
            if self.player.hp <= 0 and not self.dead:
                self.dead = True
                self.game_over()
                return
            now = pygame.time.get_ticks()
            if time.time() - self.start_time >= 30:
                self.start_time = time.time()
                self.spawn_interval = max(300, self.spawn_interval - 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        try:
                            self.pause_menu()
                        except Exception as e:
                            if str(e) == "MAIN_MENU":
                                return
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.coin.update()
            if self.player.rect.colliderect(self.coin.rect):
                self.score += 1
                if self.player.hp < self.player.max_hp:
                    self.player.hp += 10
                    if self.player.hp > self.player.max_hp:
                        self.player.hp = self.player.max_hp
                self.coin.rect.center = (random.randint(20, 780), -20)
            if now - self.last_spawn_time > self.spawn_interval:
                self.spawn_spike()
            for spike in self.spikes[:]:
                spike.update()
                if self.player.rect.colliderect(spike.rect):
                    if self.player.shield > 0:
                        self.player.shield -= self.damage
                        if self.player.shield < 0:
                            self.player.shield = 0
                    else:
                        self.player.hp -= self.damage
                        if self.player.hp < 0:
                            self.player.hp = 0
                    self.spikes.remove(spike)
                elif spike.rect.top > 600:
                    self.spikes.remove(spike)
            self.potion.update()
            if self.player.rect.colliderect(self.potion.rect):
                self.potion.activate()
            self.potion.check(self.player)
            screen.blit(self.background, (0, 0))
            self.coin.draw(screen)
            self.potion.draw(screen)
            for spike in self.spikes:
                spike.draw(screen)
            self.player.draw(screen)
            pygame.draw.rect(screen, (0, 0, 255), (10, 50, 200 * (self.player.shield / self.player.max_shield), 15))
            pygame.draw.rect(screen, (255, 255, 255), (10, 50, 200, 15), 2)
            pygame.draw.rect(screen, (255, 0, 0), (10, 70, 200 * (self.player.hp / self.player.max_hp), 15))
            pygame.draw.rect(screen, (255, 255, 255), (10, 70, 200, 15), 2)
            screen.blit(font.render(f"Score: {self.score}", True, (255, 255, 0)), (10, 10))
            screen.blit(font.render(f"HP: {self.player.hp}", True, (255, 50, 50)), (220, 70))
            screen.blit(font.render(f"Shield: {self.player.shield}", True, (100, 150, 255)), (220, 50))
            pygame.display.flip()
            clock.tick(60)

def difficulty_screen():
    global difficulty
    easy_btn = pygame.Rect(300, 250, 200, 60)
    normal_btn = pygame.Rect(300, 330, 200, 60)
    hard_btn = pygame.Rect(300, 410, 200, 60)
    back_btn = pygame.Rect(300, 490, 200, 60)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(event.pos):
                    difficulty = "easy"
                    return
                elif normal_btn.collidepoint(event.pos):
                    difficulty = "normal"
                    return
                elif hard_btn.collidepoint(event.pos):
                    difficulty = "hard"
                    return
                elif back_btn.collidepoint(event.pos):
                    return
        screen.fill((0, 0, 0))
        screen.blit(big_font.render("Сложность", True, (255, 255, 255)), (200, 120))
        pygame.draw.rect(screen, (50, 150, 50), easy_btn)
        screen.blit(font.render("ЛЁГКО", True, (255, 255, 255)), (easy_btn.x + 60, easy_btn.y + 15))
        pygame.draw.rect(screen, (50, 50, 150), normal_btn)
        screen.blit(font.render("НОРМАЛЬНО", True, (255, 255, 255)), (normal_btn.x + 35, normal_btn.y + 15))
        pygame.draw.rect(screen, (150, 50, 50), hard_btn)
        screen.blit(font.render("ТЯЖЕЛО", True, (255, 255, 255)), (hard_btn.x + 55, hard_btn.y + 15))
        pygame.draw.rect(screen, (150, 150, 50), back_btn)
        screen.blit(font.render("НАЗАД", True, (255, 255, 255)), (back_btn.x + 55, back_btn.y + 15))
        pygame.display.flip()
        clock.tick(60)

def menu_screen():
    start_button = pygame.Rect(300, 300, 200, 60)
    records_button = pygame.Rect(300, 380, 200, 60)
    skins_button = pygame.Rect(300, 460, 200, 60)
    difficulty_button = pygame.Rect(300, 540, 200, 60)
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
                if difficulty_button.collidepoint(event.pos):
                    return "difficulty"
        screen.fill((0, 0, 0))
        screen.blit(big_font.render("My Game", True, (255, 255, 255)), (200, 120))
        pygame.draw.rect(screen, (50, 150, 50), start_button)
        screen.blit(font.render("НАЧАТЬ", True, (255, 255, 255)), (start_button.x + 50, start_button.y + 15))
        pygame.draw.rect(screen, (50, 50, 150), records_button)
        screen.blit(font.render("РЕКОРДЫ", True, (255, 255, 255)), (records_button.x + 35, records_button.y + 15))
        pygame.draw.rect(screen, (150, 50, 150), skins_button)
        screen.blit(font.render("СКИНЫ", True, (255, 255, 255)), (skins_button.x + 55, skins_button.y + 15))
        pygame.draw.rect(screen, (150, 150, 50), difficulty_button)
        screen.blit(font.render("СЛОЖНОСТЬ", True, (0, 0, 0)), (difficulty_button.x + 25, difficulty_button.y + 15))
        pygame.display.flip()
        clock.tick(60)

while True:
    choice = menu_screen()
    if choice == "start":
        Game().run()
    elif choice == "records":
        Game().records_screen()
    elif choice == "skins":
        Game().skins_menu()
    elif choice == "difficulty":
        difficulty_screen()
