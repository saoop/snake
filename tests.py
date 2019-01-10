import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.tic = 1

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        screen.fill((0, 0, 0))
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] == 0:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (self.left + i * 30, self.top + j * 30, self.cell_size, self.cell_size), 1)
                elif self.board[j][i] == 1:
                    pygame.draw.circle(screen, (255, 0, 0),
                                     (self.left + i * 30 + 15, self.top + j * 30 + 15), 13, 2)
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (self.left + i * 30, self.top + j * 30, self.cell_size, self.cell_size), 1)

                else:
                    pygame.draw.line(screen, (0, 0, 255),
                                     (self.left + i * 30 + 2, self.top + j * 30 + 2), (self.left + i * 30 + 28, self.top + j * 30 + 28), 2)
                    pygame.draw.line(screen, (0, 0, 255),
                                     (self.left + i * 30 + 28, self.top + j * 30 + 2), (self.left + i * 30 + 2, self.top + j * 30 + 28), 2)
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (self.left + i * 30, self.top + j * 30, self.cell_size, self.cell_size), 1)

    def draw(self, x, y):
        for i in range(self.width):
            if i * 30 + self.left < x < self.left + (i+1) * 30:
                x = i
                break

        for i in range(self.height):
            if i * 30 + self.left < y < self.left + (i+1) * 30:
                y = i
                break

        if self.board[y][x] == 2 or self.board[y][x] == 1:
            return

        self.board[y][x] += self.tic

        self.tic = 1 if self.tic == 2 else 2


if __name__ == '__main__':
    pygame.init()
    size = width, height = 530, 300
    screen = pygame.display.set_mode(size)
    board = Board(5, 8)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    x, y = event.pos
                    board.draw(x, y)
                except Exception:
                    pass
            if event.type == pygame.QUIT:
                run = False
        board.render()
        pygame.display.flip()
    pygame.quit()
