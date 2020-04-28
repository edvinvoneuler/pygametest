import pygame


class Enemy:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("imgs/fiende_rak.png")


# Initialize pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.font.init()
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Title
pygame.display.set_caption("Shitty Space Game")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

# Sounds
player_shot_sound = pygame.mixer.Sound("rymdspelsljud/spelare_skott.wav")
enemy_death = pygame.mixer.Sound("rymdspelsljud/spelare_death.wav")
win_loop = pygame.mixer.Sound("rymdspelsljud/winjingle_1.wav")


music_loop = pygame.mixer.music.load("rymdspelsljud/edvonk_game_loop.mp3")

ambient_loop = pygame.mixer.Sound("rymdspelsljud/_space_ambience_motor_sounds_whatever.wav")
ambient_loop.set_volume(0.05)

# Player
playerImgArray = [pygame.image.load("imgs/P_L.png"), pygame.image.load("imgs/P.png"), pygame.image.load("imgs/P_R.png")]
playerImg = playerImgArray[1]
playerX = 400-32
playerY = 600-84

changeX = 0


def draw_player(x, y):
    screen.blit(playerImg, (x, y))


def wallhit_y(self):
    for array in self:
        for enemy in array:
            enemy.y += 30


# Enemy
grid = [[], [], []]
for i in range(0, 3):
    for j in range(0, 6):
        grid[i].append(Enemy(1 + 96*j, i*96))

deltaX = 0.2
enemyImg = pygame.image.load("spaceship.png")


def draw_enemy(enemy):
    screen.blit(enemy.image, (enemy.x, enemy.y))


# Bullets

shot = 0
bulletX = 0
bulletY = 0
bullet_change = 0.5

# Game loop
pygame.mixer.music.play()
pygame.mixer.Sound.play(ambient_loop, -1)
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
                changeX = -0.3
                playerImg = playerImgArray[0]
            if event.key == pygame.K_RIGHT:
                changeX = 0.3
                playerImg = playerImgArray[2]
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and changeX < 0) or (event.key == pygame.K_RIGHT and changeX > 0):
                changeX = 0
                playerImg = playerImgArray[1]

        # If keystroke is space, shoot if shot == None
        if event.type == pygame.KEYDOWN and shot == 0:
            if event.key == pygame.K_SPACE:
                shot = 1
                bulletY = playerY
                bulletX = playerX + 32
                bullet = pygame.Rect(bulletX, bulletY, 2, 4)
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
        bullet = pygame.Rect(bulletX, bulletY, 2, 4)
        pygame.draw.rect(screen, (0, 0, 0), bullet)
        if bulletY < 0:
            shot = 0

    # Update enemy

    for i in range(len(grid)-1, -1, -1):
        array = grid[i]
        for j in range(len(array)-1, -1, -1):
            enemy = array[j]
            if array[len(array)-1].x >= 800-64 and deltaX > 0:
                deltaX = -deltaX
                wallhit_y(grid)
            elif array[0].x <= 0 and deltaX < 0:
                deltaX = -deltaX
                wallhit_y(grid)
            if enemy.x + 64 > bulletX > enemy.x and enemy.y + 64 > bulletY > enemy.y and shot == 1:
                array.pop(j)
                enemy_death.play()
                shot = 0
            else:
                enemy.x += deltaX
                draw_enemy(enemy)

    if len(grid[0]) == 0 and len(grid[1]) == 0 and len(grid[2]) == 0:
        pygame.mixer.music.stop()
        screen.fill((255, 255, 255))
        draw_player(playerX, playerY)
        win_font = pygame.font.Font('freesansbold.ttf', 64)
        win_text = win_font.render("YOU WIN", True, (0, 0, 0))
        screen.blit(win_text, ((800-win_text.get_width())/2, (600-win_text.get_height())/2))

        pygame.mixer.Sound.play(win_loop)
        pygame.display.flip()
        pygame.time.wait(4000)

        running = False

    # Draw entities

    pygame.display.flip()
