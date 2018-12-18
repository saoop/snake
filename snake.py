import pygame
from pygame.locals import *
from random import randint


class Apple():
    def __init__(self):
        self.x = random()

class Square():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20

    def get_coords(self):
        return self.x, self.y

    def set_coords(self, x, y):
        self.x = x
        self.y = y
        if self.x > 500:
            self.x = 0
        if self.x < 0:
            self.x = 500
        if self.y > 300:
            self.y = 0
        if self.y < 0:
            self.y = 300


pygame.init()
size = width, height = 500, 300
screen = pygame.display.set_mode(size)
route = (0, 0)

M = pygame.USEREVENT + 1

list_of_squares = [Square(250, 150), Square(270, 150), Square(290, 150), Square(310, 150)]


def draw(route):
    screen.fill((0, 0, 0))
    first = list_of_squares[0]
    x, y = first.get_coords()
    last = list_of_squares.pop()
    last.set_coords(x + route[0], y + route[1])
    list_of_squares.insert(0, last)

    for square in list_of_squares:
        x, y = square.get_coords()
        pygame.draw.rect(screen, (0, 255, 0), (x, y, 20, 20))


running = True

while running:
    pygame.time.set_timer(M, 70)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = list_of_squares[-1].get_coords()
            print(x, y)
            list_of_squares.append(Square(x - route[0], y - route[1]))
        if event.type == M:
            x, y = list_of_squares[-1].get_coords()
            print(x, y)
            list_of_squares.append(Square(x - route[0], y - route[1]))
        if event.type == pygame.QUIT:
            running = False

    pygame.time.delay(60)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        route = (0, -10)
        # y -= 20
    elif keys[pygame.K_a]:
        route = (-10, 0)
        # x -= 20
    elif keys[pygame.K_s]:
        route = (0, 10)
        # y += 20
    elif keys[pygame.K_d]:
        route = (10, 0)
        # x += 20
    draw(route)
    pygame.display.flip()
pygame.quit()