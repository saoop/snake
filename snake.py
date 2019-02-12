# Надо сделать взрыв через частицы, спрайты мб


import pygame
from random import randint, choice
from random import randrange
import os


class Button():
    def __init__(self, x, y):
        self.width = 180
        self.height = 60  # the same in all buttons
        self.x = x
        self.y = y
        self.color = (250, 100, 100)

    def check_mouse(self):
        x, y = pygame.mouse.get_pos()
        if check_intersection(x, y, self.x,
                              self.y, self.width, self.height):
            self.color = (220, 80, 80)
        else:
            self.color = (250, 100, 100)


class GameMenu():
    def __init__(self):
        self.v = 300
        self.width = 200
        self.height = 250
        self.x = WIDTH / 2 - self.width / 2
        self.y = -HEIGHT

        self.resume_button = Button(self.x + 10, self.y + 20)
        self.quit_button = Button(self.x + 10, self.resume_button.y + self.resume_button.height + 20)

        self.button_width = self.resume_button.width
        self.button_height = self.resume_button.height


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
        self.list_snake = [Square(-100 + i * 20, 100) for i in range(4)]

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
        if 0 < abs(x - x1) <= 25 and abs(y - y1) <= 25:
            if self.route[1] == 0:
                return 0, 5 if x - x1 < 0 else 0, -5
            else:
                return 5, 0 if y - y1 < 0 else -5, 0
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
        self.HEIGHT = 20

    def get_coords(self):
        return self.x, self.y

    def set_coords(self, x, y):
        self.x = x
        self.y = y
        if self.x > WIDTH - 30:
            self.x = 0
        if self.x < 0:
            self.x = WIDTH - 30
        if self.y > HEIGHT - 10:
            self.y = 0
        if self.y < 0:
            self.y = HEIGHT - 10


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
    clock1 = pygame.time.Clock()
    red = (255, 0, 0)
    dark_red = (155, 0, 0)
    yellow = (255, 255, 0)
    dark_yellow = (155, 155, 0)
    orange = (255, 165, 0)
    arr = [[x + randint(-12, 12), y + randint(-12, 12), randint(-15, 15),
            randint(-15, 15), choice([red, yellow, orange, dark_red, dark_yellow])] for _ in range(randint(25, 35))]
    # arr[i][0] = X, arr[i][1] = Y
    l = len(arr)
    for i in range(50):  # 3 seconds
        n = clock1.tick()
        for j in range(l):
            print(arr[j][0])
            arr[j][0] += arr[j][2] * n / 1000
            arr[j][1] += arr[j][3] * n / 1000
            pygame.draw.rect(screen, arr[j][4], (arr[j][0], arr[j][1], 5, 5))
            pygame.display.flip()
        pygame.time.delay(60)


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
    text_best_score_x = WIDTH // 2 - text_best_score.get_width() // 2
    text_best_score_y = HEIGHT // 2 - text_best_score.get_height() // 2 - 50
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
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
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))


def check_intersection(x, y, x1, y1, w, h):
    if x1 <= x <= x1 + w and y1 <= y <= y1 + h:
        return True
    return False


def draw_game_menu():
    screen.fill((0, 0, 0))
    if game_menu.y < 0:
        a = game_menu.v * clock.tick() / 1000
        game_menu.y += a
        game_menu.resume_button.y += a
        game_menu.quit_button.y += a
    pygame.draw.rect(screen, (250, 100, 100), (game_menu.x, game_menu.y, game_menu.width, game_menu.height), 10)

    game_menu.resume_button.check_mouse()

    pygame.draw.rect(screen, game_menu.resume_button.color, (game_menu.resume_button.x,
                     game_menu.resume_button.y, game_menu.button_width, game_menu.button_height))
    font = pygame.font.Font(None, 60)
    text = font.render('Resume', 1, (10, 10, 10))
    screen.blit(text, (game_menu.resume_button.x, game_menu.resume_button.y))

    game_menu.quit_button.check_mouse()

    pygame.draw.rect(screen, game_menu.quit_button.color, (game_menu.quit_button.x,
                     game_menu.quit_button.y, game_menu.button_width, game_menu.button_height))
    text2 = font.render('Quit', 1, (10, 10, 10))
    screen.blit(text2, (game_menu.quit_button.x, game_menu.quit_button.y))


def draw_score():
    if start:
        font = pygame.font.Font(None, 50)
        text = font.render(str(score), 1, (100, 255, 100))
        screen.blit(text, (500, 10))


def draw(route):
    global current_apple
    global is_game_over

    if not is_game_over:
        is_boom_draw = False
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

        x2, y2 = snake[0].get_coords()  # coords of first square

        pygame.draw.rect(screen, (10, 180, 10), (x2, y2, 20, 20))

        for square in snake[1:]:
            x1, y1 = square.get_coords()
            pygame.draw.rect(screen, (0, 255, 0), (x1, y1, 20, 20))

        draw_score()
        for square in snake[2:]:
            x1, y1 = square.get_coords()
            if y1 - 10 == y2 and x2 == x1 or y1 == y2 and x2 + 10 == x1 \
                    or y1 + 10 == y2 and x2 == x1 or y1 == y2 and x2 - 10 == x1:
                is_game_over = True
                is_boom_draw = True
                pygame.time.delay(200)
                break

        if is_evil_snake_appeared:
            for square in snake[:]:
                x1, y1 = square.get_coords()
                if evil_snake.check_go(x1, y1):
                    set_route = evil_snake.check_go(x1, y1)

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

            if check_eat(evil_snake[0].x, evil_snake[0].y, evil_snake.list_snake):
                current_apple = Apple()

        if is_boom_draw:
            draw_boom()  # я так сделал, чтобы сначала нарисовались обе змейки, а только потом произошел взрыв
    else:
        draw_game_over()
        draw_cursor()


def draw_cursor():
    x, y = pygame.mouse.get_pos()
    cursor.rect.x = x
    cursor.rect.y = y
    all_sprites.draw(screen)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def set_standart():
    global start, end, is_game_over, route, time, score, time_int, snake, is_evil_snake_appeared, game_menu
    start = True
    end = False
    game_menu = GameMenu()
    is_evil_snake_appeared = False
    is_game_over = False
    route = (-10, 0)
    time = 65
    score = 0
    time_int = 65
    snake = Snake()


if __name__ == '__main__':
    pygame.init()

    pygame.mouse.set_visible(False)

    size = WIDTH, HEIGHT = 530, 300
    screen = pygame.display.set_mode(size)
    running = True
    route = (-10, 0)
    start = False

    is_evil_snake_appeared = False
    snake = Snake()
    score = 0

    all_sprites = pygame.sprite.Group()
    cursor = pygame.sprite.Sprite()
    cursor.image = load_image('cursor.png')
    cursor.rect = cursor.image.get_rect()
    all_sprites.add(cursor)

    game_menu = GameMenu()

    clock_for_boom = pygame.time.Clock()

    end = False
    is_menu = False

    delta = 10

    time = 65
    time_int = 65

    is_game_over = False
    current_apple = Apple()

    while running:
        pygame.time.delay(time_int)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                if not start:
                    x, y = event.pos
                    if 150 <= x <= 350 and 100 <= y <= 200:
                        set_standart()

                elif end:
                    start = False

                elif is_menu:
                    x, y = event.pos
                    x1, y1 = game_menu.resume_button.x, game_menu.resume_button.y
                    if check_intersection(x, y, x1, y1, game_menu.button_width, game_menu.button_height):
                        is_menu = False
                        game_menu = GameMenu()
                    x1, y1 = game_menu.quit_button.x, game_menu.quit_button.y

                    if check_intersection(x, y, x1, y1, game_menu.button_width, game_menu.button_height):
                        is_menu = False
                        is_game_over = True
                        game_menu = GameMenu()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if not is_menu and start and not is_game_over:
                        clock = pygame.time.Clock()
                        is_menu = True
                    elif start and is_menu:
                        is_menu = False
                        game_menu = GameMenu()

            if event.type == pygame.QUIT:
                running = False

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

        if start and not is_menu:
            draw(route)
        elif is_menu:
            draw_game_menu()
            draw_cursor()
        else:
            draw_menu()
            draw_cursor()
        pygame.display.flip()
    pygame.quit()
