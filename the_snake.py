
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
# Количество клеток по ширине поля:
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
# Количество клеток по высоте поля:
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
choice_direction = (UP, DOWN, LEFT, RIGHT)

# Центр экрана:
MID = ((SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
       (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20
# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс"""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR, position=MID):
        """Инициализируем начальные данные по объекту"""
        # position — позиция объекта на игровом поле;
        # body_color — цвет объекта
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Метод заглушки, далее в методе рисуем объекты"""
        raise NotImplementedError('Метод draw не реализован '
                                  f'в {self.__class__.__name__}')


class Apple(GameObject):
    """Класс описывающий объект - яблоко"""

    def __init__(self, body_color=APPLE_COLOR, position=None,
                 occupied_position=None):
        """Инициализируем начальные данные по объекту"""
        super().__init__(body_color=body_color, position=position)
        occupied_position = occupied_position or []
        self.randomize_position(occupied_position)

    # Добавим параметр (список занятых ячеек)
    def randomize_position(self, occupied_position):
        """Создаем объект яблоко, его позиция"""
        """определяться случайным образом"""
        while True:
            x_idx = randint(0, GRID_WIDTH - 1)  # Индекс клетки по x
            y_idx = randint(0, GRID_HEIGHT - 1)  # Индекс клетки по y
            x = x_idx * GRID_SIZE
            y = y_idx * GRID_SIZE
            new_position = (x, y)
            if new_position not in occupied_position:
                self.position = new_position
                break

    def draw(self):
        """Метод отрисовки яблока на экране"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывает объект змейка"""

    def __init__(self, body_color=SNAKE_COLOR, position=MID):
        """Инициализируем начальные данные по объекту"""
        super().__init__(body_color=body_color, position=position)
        self.reset()
        self.direction = RIGHT

    def get_head_position(self):
        """Получаем значение положения головы"""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновление текущего движения змейки"""
        self.direction = new_direction

    def move(self):
        """Описываем, как змейка будет двигаться"""
        # Распаковываем позицию головы змейки на составляющие x и y
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        # Рассчитываем новые координаты сразу с ограничением
        # по остатку от деления
        new_pos = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_pos)
        self.last = self.positions.pop()

    def grow(self):
        """Возвращает последний удаленный сегмент обратно в хвост"""
        """при поедании яблока"""
        if self.last is not None:
            self.positions.append(self.last)
            self.last = None

    def draw(self):
        """Отображаем экземпляр в игре"""
        rect = (pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента, закрашиваем клетку черным
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние при столкновении"""
        self.length = 1
        self.positions = [self.position]
        # Задаем движение змейки в неизвестном напрлавлении
        self.direction = choice(choice_direction)
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Метод обработки нажатия клавиш пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Основной метод вызова игры"""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(APPLE_COLOR, occupied_position=snake.positions)
    # Проверка, что яблоко не появилось в одном месте со змейкой
    while True:
        handle_keys(snake)
        clock.tick(GRID_SIZE)
        snake.move()
        # Увеличиваем хвост, когда сьели яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.grow()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
