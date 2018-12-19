import pygame
from pygame.locals import *
from random import randint
from random import randrange


class Apple():
    def __init__(self):
        self.x = randrange(0, 500, 20)
        self.y = randrange(0, 300, 20)
        l = map(lambda x: x.get_coords()[0], list_of_squares)
        while self.x in l:
            self.x = randrange(0, 500, 20)
        r = map(lambda x: x.get_coords()[1], list_of_squares)
        while self.y in r:
            self.y = randrange(0, 300, 20)

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
size = width, height = 530, 300
screen = pygame.display.set_mode(size)
route = (-10, 0)

score = 0

is_game_over = False

M = pygame.USEREVENT + 1

list_of_squares = [Square(250, 150), Square(270, 150), Square(290, 150), Square(310, 150)]
current_apple = Apple()


def add_square():
    x, y = list_of_squares[-1].get_coords()
    list_of_squares.append(Square(x - route[0], y - route[1]))
    list_of_squares.append(Square(x - 2 * route[0], y - 2 * route[1]))


def check_eat(x, y):
    global score
    if current_apple.x <= x < current_apple.x + 20 and current_apple.y <= y < current_apple.y + 20 or\
            x <= current_apple.x < x + 20 and y <= current_apple.y < y + 20:
        add_square()
        score += 1
        return True

    return False


def draw_game_over():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("GAMEOVER "
                       "Your score: " + str(score), 1, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def draw_score():
    font = pygame.font.Font(None, 50)
    text = font.render(str(score), 1, (100, 255, 100))
    screen.blit(text, (500, 10))


def draw(route):
    global current_apple
    global is_game_over

    if not is_game_over:
        screen.fill((0, 0, 0))
        first = list_of_squares[0]
        x, y = first.get_coords()
        last = list_of_squares.pop()

        last.set_coords(x + route[0], y + route[1])
        list_of_squares.insert(0, last)
        if check_eat(x, y):
            current_apple = Apple()

        pygame.draw.rect(screen, (255, 0, 0), (current_apple.x, current_apple.y, 20, 20))

        x2, y2 = list_of_squares[0].get_coords()

        pygame.draw.rect(screen, (10, 180, 10), (x2, y2, 20, 20))

        for square in list_of_squares[1:]:
            x1, y1 = square.get_coords()
            pygame.draw.rect(screen, (0, 255, 0), (x1, y1, 20, 20))

        draw_score()

        for square in list_of_squares[2:]:
            x1, y1 = square.get_coords()
            if y1 - 10 == y2 and x2 == x1 or y1 == y2 and x2 + 10 == x1 \
                    or y1 + 10 == y2 and x2 == x1 or y1 == y2 and x2 - 10 == x1:
                is_game_over = True
                pygame.time.delay(3000)
                print(x1, y1, x2, y2)
                break
    else:
        draw_game_over()

running = True

while running:
    pygame.time.set_timer(M, 70)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.time.delay(60)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and route != (0, 10):
        route = (0, -10)
    elif keys[pygame.K_a] and route != (10, 0):
        route = (-10, 0)
    elif keys[pygame.K_s] and route != (0, -10):
        route = (0, 10)
    elif keys[pygame.K_d] and route != (-10, 0):
        route = (10, 0)

    draw(route)
    pygame.display.flip()
pygame.quit()
