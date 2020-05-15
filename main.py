import pygame
import random


class Enemy:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("imgs/fiende_rak.png")
        self.no_shot = 0
        self.shots = []

    def rand_shot(self):
        if random.randrange(0, 100) <= self.no_shot and len(self.shots) <= 1:
            self.shots.append(pygame.Rect(self.x+30, self.y+64, 4, 8))
            self.no_shot = 0
        else:
            self.no_shot += .01

    def check_shot(self):
        for i in range(len(self.shots)-1, 0, -1):
            if self.shots[i].y > HEIGHT:
                self.shots.pop(i)
            elif self.shots[i].y >= playerY and playerX < self.shots[i].x < playerX + 64:
                global hp
                hp -= 1
                self.shots.pop(i)
                print(hp)
            else:
                self.shots[i] = self.shots[i].move(0, 5)
                pygame.draw.rect(screen, (255, 0, 0), self.shots[i])


class EnemyFreighter:

    def __init__(self):
        self.x = 800
        self.y = 0
        self.image = pygame.Surface((128, 64))
        self.image.fill((255, 0, 0))
        self.speed = 2
        self.time_since_last = 0

    def update(self, surface):
        self.x += self.speed
        surface.blit(self.image, (self.x, self.y))
        self.time_since_last += 1

        if self.time_since_last == 60 * 10:
            self.x = -128
            self.time_since_last = -10
            ambient_loop.play()

    def check_hit(self, bullet_x, bullet_y, shot):

        if self.x < bullet_x < self.x + 128 and self.y < bullet_y < self.y + 64 and shot == 1:
            global turn_rate
            global power_up_timer
            self.x = 800
            turn_rate = 2*turn_rate
            power_up.play()
            power_up_timer = 0
            ambient_loop.stop()
        elif WIDTH < self.x:
            ambient_loop.stop()


class EnemyExplosion:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_array = image_array
        self.img = None
        self.index = -1
        self.counter = 0

    def update(self):
        if self.counter % 2 == 0:
            self.index += 1
            if self.index > len(self.image_array) - 1:
                return False
            self.img = image_array[self.index]

        self.counter += 1
        print(self.counter)
        pygame.Surface.blit(screen, self.img, (self.x, self.y))


def you_lose():

    pygame.mixer.music.stop()
    ambient_loop.stop()
    screen.fill((255, 255, 255))
    lose_font = pygame.font.Font('freesansbold.ttf', 64)
    lose_text = lose_font.render("YOU LOSE", True, (0, 0, 0))
    screen.blit(lose_text, ((WIDTH - lose_text.get_width()) / 2, (HEIGHT - lose_text.get_height()) / 2))

    pygame.mixer.Sound.play(game_over)
    pygame.display.flip()
    pygame.time.wait(4000)


def you_win():
    pygame.mixer.music.stop()
    ambient_loop.stop()
    screen.fill((255, 255, 255))
    win_font = pygame.font.Font('freesansbold.ttf', 64)
    win_text = win_font.render("YOU WIN", True, (0, 0, 0))
    screen.blit(win_text, ((WIDTH - win_text.get_width()) / 2, (HEIGHT - win_text.get_height()) / 2))

    pygame.mixer.Sound.play(win_loop)
    pygame.display.flip()
    pygame.time.wait(4000)


def draw_enemy(enemy):
    screen.blit(enemy.image, (enemy.x, enemy.y))


def draw_player(x, y):
    screen.blit(playerImg, (x, y))


def wallhit_y(self):
    for array in self:
        for enemy in array:
            enemy.y += 48


WIDTH = 800
HEIGHT = 1000

# Initialize pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.font.init()
pygame.init()


clock = pygame.time.Clock()

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title
pygame.display.set_caption("Shitty Space Game")
icon = pygame.image.load("imgs/P.png")
pygame.display.set_icon(icon)

# Sounds
player_shot_sound = pygame.mixer.Sound("rymdspelsljud/spelare_skott.wav")
enemy_death = pygame.mixer.Sound("rymdspelsljud/spelare_death.wav")
win_loop = pygame.mixer.Sound("rymdspelsljud/winjingle_1.wav")
game_over = pygame.mixer.Sound("rymdspelsljud/_game_over.wav")
power_up = pygame.mixer.Sound("rymdspelsljud/spelare_powerup.wav")

music_loop = pygame.mixer.music.load("rymdspelsljud/gregurtsmusik_bitcrushed.wav")

ambient_loop = pygame.mixer.Sound("rymdspelsljud/_space_ambience_motor_sounds_whatever.wav")

# Player
playerImgArray = [pygame.image.load("imgs/P_L.png").convert_alpha(), pygame.image.load("imgs/P.png").convert_alpha(), pygame.image.load("imgs/P_R.png").convert_alpha()]
playerImg = playerImgArray[1]
playerX = WIDTH/2-32
playerY = HEIGHT-84
hp = 3
power_up_timer = 0

# Player shots
shot = 0
bulletX = 0
bulletY = 0
bullet_change = 10


changeX = 0
turn_rate = 5


# Create enemies in a grid
grid = [[], [], []]
for i in range(0, 3):
    for j in range(0, 6):
        grid[i].append(Enemy(1 + 96*j, 64 + (i*96)))

# Enemy speed
deltaX = 2

enemyImg = pygame.image.load("imgs/P.png")

# Image array for explosion animation
# TODO: Automate reading images from folders or make a sprite sheet reader
image_array = [pygame.image.load("imgs/explosion/explosionAgif11-0.png").convert_alpha(),pygame.image.load("imgs/explosion/explosionAgif11-1.png").convert_alpha(), pygame.image.load("imgs/explosion/explosionAgif11-2.png").convert_alpha(),
               pygame.image.load("imgs/explosion/explosionAgif11-3.png").convert_alpha(), pygame.image.load("imgs/explosion/explosionAgif11-3.png").convert_alpha(), pygame.image.load("imgs/explosion/explosionAgif11-4.png").convert_alpha(),
               pygame.image.load("imgs/explosion/explosionAgif11-5.png").convert_alpha(), pygame.image.load("imgs/explosion/explosionAgif11-6.png").convert_alpha(), pygame.image.load("imgs/explosion/explosionAgif11-7.png").convert_alpha(),
               pygame.image.load("imgs/explosion/explosionAgif11-8.png").convert_alpha(), pygame.image.load("imgs/explosion/explosionAgif11-9.png").convert_alpha(),pygame.image.load("imgs/explosion/explosionAgif11-10.png").convert_alpha(),
               pygame.image.load("imgs/explosion/explosionAgif11-11.png").convert_alpha(),pygame.image.load("imgs/explosion/explosionAgif11-12.png").convert_alpha(), pygame.image.load("imgs/explosion/explosionAgif11-13.png").convert_alpha(),
               pygame.image.load("imgs/explosion/explosionAgif11-14.png").convert_alpha()]
explosions = []

# Game loop
pygame.mixer.music.play(-1)

freighter = EnemyFreighter()

running = True
while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed, check if left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                changeX = -turn_rate
                playerImg = playerImgArray[0]
            if event.key == pygame.K_RIGHT:
                changeX = turn_rate
                playerImg = playerImgArray[2]
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and changeX < 0) or (event.key == pygame.K_RIGHT and changeX > 0):
                changeX = 0
                playerImg = playerImgArray[1]

        # If keystroke is space, shoot if shot == 0
        if event.type == pygame.KEYDOWN and shot == 0:
            if event.key == pygame.K_SPACE:
                shot = 1
                bulletY = playerY
                bulletX = playerX + 30
                bullet = pygame.Rect(bulletX, bulletY, 4, 8)
                pygame.draw.rect(screen, (0, 0, 0), bullet)
                pygame.mixer.Sound.play(player_shot_sound)

    # Update entities #

    # Update player

    playerX += changeX
    if playerX < 0:
        playerX = 0
    elif playerX > 800-64:
        playerX = 736

    draw_player(playerX, playerY)

    # Update bullet

    if shot == 1:
        bulletY -= bullet_change
        bullet = pygame.Rect(bulletX, bulletY, 4, 8)
        pygame.draw.rect(screen, (0, 255, 0), bullet)
        if bulletY < 0:
            shot = 0

    # Update enemy
    for i in range(len(grid)):

        if len(grid[i]) > 0 and grid[i][len(grid[i])-1].x > 800-64 and deltaX > 0:
            wallhit_y(grid)
            deltaX = -deltaX

        elif 0 < len(grid[i]) and grid[i][0].x < 0 and deltaX < 0:
            wallhit_y(grid)
            deltaX = -deltaX

        # If enemies reach too far down, end game.
        elif 0 < len(grid[i]) and grid[i][0].y > HEIGHT-300:
            you_lose()
            running = False
            pygame.quit()

    for i in range(len(grid)-1, -1, -1):
        array = grid[i]
        for j in range(len(array)-1, -1, -1):
            enemy = array[j]
            enemy.rand_shot()
            enemy.check_shot()
            if enemy.x + 64 > bulletX > enemy.x and enemy.y + 64 > bulletY > enemy.y and shot == 1:
                array.pop(j)
                enemy_death.play()
                explosions.append(EnemyExplosion(enemy.x, enemy.y))
                print(explosions)
                shot = 0
            else:
                enemy.x += deltaX
                draw_enemy(enemy)

    if power_up_timer == 60 * 10:
        turn_rate = 5
    power_up_timer += 1

    for i in range(len(explosions)-1, -1, -1):
        if explosions[i].update() is False:
            explosions.pop(i)

    freighter.check_hit(bulletX, bulletY, shot)
    freighter.update(screen)

    # Check game over states

    if hp == 0:
        you_lose()
        running = False

    elif len(grid[0]) == 0 and len(grid[1]) == 0 and len(grid[2]) == 0:
        you_win()
        running = False

    pygame.display.flip()
    clock.tick(60)
