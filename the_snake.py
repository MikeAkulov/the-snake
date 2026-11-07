
from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс"""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """Инициализируем начальные данные по объекту"""
        # position — позиция объекта на игровом поле;
        # body_color — цвет объекта
        self.position = (
            (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
            (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        )  # центр экрана
        self.body_color = body_color

    def draw(self):
        """Метод заглушки, далее в методе рисуем объекты"""
        pass


class Apple(GameObject):
    """Класс описывающий объект - яблоко"""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализируем начальные данные по объекту"""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Создаем объект яблоко, его позиция"""
        """определяться случайным образом"""
        x_idx = randint(0, GRID_WIDTH - 1)  # Индекс клетки по x
        y_idx = randint(0, GRID_HEIGHT - 1)  # Индекс клетки по y
        x = x_idx * GRID_SIZE
        y = y_idx * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Метод отрисовки яблока на экране"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывает объект змейка"""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализируем начальные данные по объекту"""
        super().__init__(body_color=body_color)
        self.length = 1
        self.next_direction = None
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def get_head_position(self):
        """Получаем значение положения головы"""
        return self.positions[0]

    def update_direction(self):
        """Обновление текущего движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Описываем, как змейка будет двигаться"""
        head = self.get_head_position()
        x, y = head  # Запомнили в переменные координаты головы змейки
        # Смена координат в зависимости от направления
        # Вычисляем новую позицию
        if self.direction == UP:
            new_pos = (x, y - GRID_SIZE)
        elif self.direction == DOWN:
            new_pos = (x, y + GRID_SIZE)
        elif self.direction == LEFT:
            new_pos = (x - GRID_SIZE, y)
        elif self.direction == RIGHT:
            new_pos = (x + GRID_SIZE, y)
        else:
            new_pos = head

        # Перемещение змейки за предел поля, телепортируем ее
        new_pos = (new_pos[0] % SCREEN_WIDTH, new_pos[1] % SCREEN_HEIGHT)
        self.positions.insert(0, new_pos)

        # Удаляем хвост, если длина списка больше текущей длины змейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отображаем экземпляр в игре"""
        for position in self.positions[1:]:
            # Отрисовываем все добавленные части змейки на поле
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента, закрашиваем клетку черным
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние при столкновении"""
        self.length = 1
        self.position = ((SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
                         (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE)
        self.positions = [self.position]
        # Задаем движение змейки в неизвестном напрлавлении
        self.direction = choice(choice_direction)
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Метод обработки нажатия клавиш пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной метод вызова игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    screen.fill(BOARD_BACKGROUND_COLOR)
    # Проверка, что яблоко не появилось в одном месте со змейкой
    while apple.position in snake.positions:
        apple.randomize_position()
    while True:
        handle_keys(snake)
        clock.tick(20)
        snake.update_direction()
        snake.move()
        # Увеличиваем хвост, когда сьели яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Яблоко продолжило появлятся на поле
            while apple.position in snake.positions:
                apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

# Функция обработки действий пользователя
