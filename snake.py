import pygame
from pygame.locals import *
from random import randint, choice
from random import randrange


class Snake():
    def __init__(self):
        self.list_snake = [Square(100 + i * 20, 100) for i in range(3)]
        self.delta = 10

    def __getitem__(self, item):
        return self.list_snake[item]

    def pop(self):
        return self.list_snake.pop()

    def insert(self, i, elm):
        self.list_snake.insert(i, elm)

    def append(self, elm):
        self.list_snake.append(elm)


class EvilSnake(Snake):
    def __init__(self):
        super().__init__()
        self.delta = 5
        self.true_delta = 5.0

        if current_apple.x == self.list_snake[0].x:
            if current_apple.y < self.list_snake[0].y:
                self.route = (0, -self.delta)
            elif current_apple.y > self.list_snake[0].y:
                self.route = (0, self.delta)
        else:
            if current_apple.x < self.list_snake[0].x:
                self.route = (-self.delta, 0)
            elif current_apple.x > self.list_snake[0].x:
                self.route = (self.delta, 0)

    def update_route(self, set_this_route=None):
        if set_this_route != None:
            self.route = set_this_route
            print('sd')
        else:
            if current_apple.x == self.list_snake[0].x:
                if current_apple.y < self.list_snake[0].y:
                    self.route = (0, -self.delta)
                elif current_apple.y > self.list_snake[0].y:
                    self.route = (0, self.delta)
            else:
                if current_apple.x < self.list_snake[0].x:
                    self.route = (-self.delta, 0)
                elif current_apple.x > self.list_snake[0].x:
                    self.route = (self.delta, 0)

    def check_go(self, x, y):
        x1, y1 = self.list_snake[0].get_coords()
        if abs(y - y1) <= 20 and abs(x - x1) <= 20:
            if self.route[0] == 5 or self.route[0] == -5:
                return 0, -5
            else:
                return -5, 0
        return None

    def set_route(self, route):
        self.route = route

    def update_speed(self):
        self.true_delta += 0.2 * score
        self.delta = int(self.true_delta)


class Apple():
    def __init__(self):
        self.x = randrange(0, 500, 20)
        self.y = randrange(0, 300, 20)
        l = map(lambda x: x.get_coords()[0], snake)
        while self.x in l:
            self.x = randrange(0, 500, 20)
        r = map(lambda x: x.get_coords()[1], snake)
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
        if self.x > width - 30:
            self.x = 0
        if self.x < 0:
            self.x = width - 30
        if self.y > height:
            self.y = 0
        if self.y < 0:
            self.y = height


def add_square(array):
    x, y = array[-1].get_coords()
    array.append(Square(x - route[0], y - route[1]))
    array.append(Square(x - 2 * route[0], y - 2 * route[1]))


def check_eat(x, y, array, name='evil'):
    global score, time_int, time
    if current_apple.x <= x < current_apple.x + 20 and current_apple.y <= y < current_apple.y + 20 or\
            x <= current_apple.x < x + 20 and y <= current_apple.y < y + 20:
        add_square(array)
        if name == 'me':
            score += 1
        time /= 1.01
        time_int = int(time)

        return True

    return False


def draw_boom():
    x, y = snake[0].get_coords()
    pygame.time.delay(600)
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 20, 20))
    pygame.display.flip()
    pygame.time.delay(200)
    pygame.draw.rect(screen, (255, 0, 0), (x - 5, y - 5, 30, 30), 10)
    pygame.display.flip()
    pygame.time.delay(200)
    pygame.draw.rect(screen, (255, 255, 0), (x - 10, y - 10, 40, 40), 5)
    pygame.display.flip()
    pygame.time.delay(500)


def draw_game_over():
    global end
    end = True

    best_score = score
    with open('best score.txt', 'r', encoding="utf8") as file:
        a = int(file.read())
        if score < a:
            best_score = a

    with open('best score.txt', 'w') as file:
        file.write(str(best_score))
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("GAMEOVER Your score: " + str(score), 1, (100, 255, 100))

    text_best_score = font.render('Best score: ' + str(best_score), 1, (50, 200, 50))
    text_best_score_x = width // 2 - text_best_score.get_width() // 2
    text_best_score_y = height // 2 - text_best_score.get_height() // 2 - 50
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    screen.blit(text_best_score, (text_best_score_x, text_best_score_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)


def draw_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Start", 1, (250, 100, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))


def draw_score():
    if start:
        font = pygame.font.Font(None, 50)
        text = font.render(str(score), 1, (100, 255, 100))
        screen.blit(text, (500, 10))


def draw(route):
    global current_apple
    global is_game_over

    if not is_game_over:
        screen.fill((0, 0, 0))
        first = snake[0]
        x, y = first.get_coords()
        last = snake.pop()

        set_route = None

        last.set_coords(x + route[0], y + route[1])
        snake.insert(0, last)
        if check_eat(x, y, snake, name='me'):
            current_apple = Apple()

        pygame.draw.rect(screen, (255, 0, 0), (current_apple.x, current_apple.y, 20, 20))

        x2, y2 = snake[0].get_coords()  #coords of first square

        pygame.draw.rect(screen, (10, 180, 10), (x2, y2, 20, 20))

        for square in snake[1:]:
            x1, y1 = square.get_coords()
            if is_evil_snake_appeared:
                if evil_snake.check_go(x1, y1) != None:
                    set_route = evil_snake.check_go(x1, y1)
                    print('1')

            pygame.draw.rect(screen, (0, 255, 0), (x1, y1, 20, 20))

        draw_score()

        for square in snake[2:]:
            x1, y1 = square.get_coords()
            if y1 - 10 == y2 and x2 == x1 or y1 == y2 and x2 + 10 == x1 \
                    or y1 + 10 == y2 and x2 == x1 or y1 == y2 and x2 - 10 == x1:
                is_game_over = True
                draw_boom()
                pygame.time.delay(3000)
                print(x1, y1, x2, y2)
                break

        if is_evil_snake_appeared:

            for square in evil_snake.list_snake:
                x, y = square.get_coords()
                pygame.draw.rect(screen, (255, 255, 100), (x, y, 20, 20))

            evil_snake.update_route(set_route)
            last = evil_snake.list_snake.pop()
            x, y = evil_snake.list_snake[0].x, evil_snake.list_snake[0].y
            last.set_coords(x + evil_snake.route[0], y + evil_snake.route[1])
            evil_snake.list_snake.insert(0, last)

            for square in evil_snake.list_snake:
                x, y = square.get_coords()
                if x <= x2 < x + 20 and y <= y2 < y + 20 or\
            x2 <= x < x2 + 20 and y2 <= y < y2 + 20:
                    is_game_over = True
                    draw_boom()
                    break

            if check_eat(x, y, evil_snake.list_snake):
                current_apple = Apple()
    else:
        draw_game_over()


def set_standart():
    global start, end, is_game_over, route, time, score, time_int, snake, is_evil_snake_appeared
    start = True
    end = False
    is_evil_snake_appeared = False
    is_game_over = False
    route = (-10, 0)
    time = 65
    score = 0
    time_int = 65
    snake = Snake()


running = True
if __name__ == '__main__':
    pygame.init()
    size = width, height = 530, 300
    screen = pygame.display.set_mode(size)
    route = (-10, 0)
    start = False

    is_evil_snake_appeared = False
    snake = Snake()
    score = 0

    end = False

    delta = 10

    time = 65
    time_int = 65

    is_game_over = False
    current_apple = Apple()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and not start:
                x, y = event.pos
                if 150 <= x <= 350 and 100 <= y <= 200:
                    set_standart()

            if event.type == pygame.MOUSEBUTTONDOWN and end:
                start = False

            if event.type == pygame.QUIT:
                running = False

        pygame.time.delay(time_int)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and route != (0, delta):
            route = (0, -delta)
        elif keys[pygame.K_a] and route != (delta, 0):
            route = (-delta, 0)
        elif keys[pygame.K_s] and route != (0, -delta):
            route = (0, delta)
        elif keys[pygame.K_d] and route != (-delta, 0):
            route = (delta, 0)

        if score == 2:
            evil_snake = EvilSnake()
            is_evil_snake_appeared = True

        if start:
            draw(route)
        else:
            draw_menu()
        pygame.display.flip()
    pygame.quit()
