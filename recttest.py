import pygame

white = (255, 255, 255)
black = (0, 0, 0)

gameDisplay = pygame.display.set_mode((800, 600))

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, (0, 0, 0), [100, 100, 10, 10])

    pygame.display.update()
