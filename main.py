import pygame


class Enemy:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("spaceship.png")


# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((500, 300))

# Title
pygame.display.set_caption("Shitty Space Game")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("rocket.png")
playerX = 250-16
playerY = 250

changeX = 0


def draw_player(x, y):
    screen.blit(playerImg, (x, y))


def wallhit_y(self):
    for array in self:
        for enemy in array:
            enemy.y += 10


# Enemy
grid = [[], [], []]
for i in range(0, 3):
    for j in range(0, 7):
        grid[i].append(Enemy(1 + 48*j, i*50))

deltaX = 0.2
enemyImg = pygame.image.load("spaceship.png")


def draw_enemy(enemy):
    screen.blit(enemy.image, (enemy.x, enemy.y))


shot = 0
shot_change = 1
shotY = 100000000
shotX = 100000000

# Game loop
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
            if event.key == pygame.K_RIGHT:
                changeX = 0.3
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and changeX < 0) or (event.key == pygame.K_RIGHT and changeX > 0):
                changeX = 0

        # If keystroke is space, shoot if shot == None
        if event.type == pygame.KEYDOWN and shot == 0:
            if event.key == pygame.K_SPACE:
                print("space")
                shot = 1
                shotY = playerY + 16
                shotX = playerX + 16

    # Update entities
    playerX += changeX
    if playerX < 0:
        playerX = 0
    elif playerX > 500-32:
        playerX = 468

    shotY -= shot_change

    wall = 0
    for array in grid:
        for enemy in array:
            if array[len(array)-1].x >= 500-32 and deltaX > 0:
                deltaX = -deltaX
                wallhit_y(grid)
            elif array[0].x <= 0 and deltaX < 0:
                deltaX = -deltaX
                wallhit_y(grid)
            enemy.x += deltaX
            draw_enemy(enemy)
    draw_player(playerX, playerY)
    pygame.display.update()
