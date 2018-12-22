import pygame
pygame.init()
size = width, height = 530, 300
screen = pygame.display.set_mode(size)
route = (-10, 0)
start = False

score = 0

end = False

delta = 10

time = 65
time_int = 65

is_game_over = False


def draw_boom():
    print('asd')
    x, y = 10, 20
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 20, 20))
    pygame.display.flip()
    print('1')
    pygame.time.delay(1000)
    pygame.draw.rect(screen, (255, 255, 0), (x - 10, y - 10, 40, 40))
    pygame.display.flip()
    print('2')
    pygame.time.delay(1000)
    pygame.draw.rect(screen, (255, 255, 0), (x - 20, y - 20, 60, 60))
    pygame.display.flip()
    print('3')
    pygame.time.delay(2000)


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and end:
            start = False

        if event.type == pygame.QUIT:
            run = False

    draw_boom()
    pygame.display.flip()
pygame.quit()