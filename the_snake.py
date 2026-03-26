import sys
from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (37, 40, 80)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (204, 0, 37)
SNAKE_COLOR = (0, 117, 57)
SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

clock = pg.time.Clock()


class GameObject:
    """Создание родительского класса GameObject."""

    def __init__(self, position=CENTER_POSITION, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw_objects(self,
                     position,
                     fill_color=None,
                     border_color=BORDER_COLOR
                     ):
        """Дочерний метод для отрисовки объектов."""
        color_fill = fill_color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color_fill, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Дочерний метод для отрисовки объектов."""


class Apple(GameObject):
    """Создание класса Apple с указанием родительского класса GameObject."""

    def __init__(self, body_color=APPLE_COLOR, occupied_positions=None):
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions or [])

    def draw(self):
        """Метод для отрисовки яблока."""
        self.draw_objects(self.position)

    def randomize_position(self, occupied_positions=None):
        """Метод для установки рандомной позиции яблока."""
        occupied_positions = occupied_positions or []
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            """Проверка координат для предотвращения спавна яблока в змее."""
            if self.position not in occupied_positions:
                break


class Snake(GameObject):
    """Создание класса Snake с указанием родительского класса GameObject."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Метод для обновления направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для движения головы змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод для отрисовки змейки."""
        for position in self.positions:
            self.draw_objects(position)

        if self.last is not None:
            self.draw_objects(
                self.last,
                fill_color=BOARD_BACKGROUND_COLOR,
                border_color=BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Метод для получения позиции головы."""
        return self.positions[0]

    def reset(self):
        """Метод для збрасывания змейки в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция обработки нажатий клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()
            elif event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция запуска цикла, иинициализации классов
    и создания экземпляров классов.
    """
    pg.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(occupied_positions=snake.positions)

    while True:
        pg.display.set_caption(f'Змейка | Очки: {snake.length}')
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            if apple.position in snake.positions:
                apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
