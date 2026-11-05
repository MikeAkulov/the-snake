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
    '''Основной класс игры'''
    def __init__(self, body_color):
        # position — позиция объекта на игровом поле;
        # body_color — цвет объекта
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # центр экрана
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self, body_color):
        super().__init__(body_color)
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        x_idx = random.randint(0, GRID_WIDTH - 1)  # Индекс клетки по x
        y_idx = random.randint(0, GRID_HEIGHT - 1)  # Индекс клетки по y
        x = x_idx * GRID_SIZE + GRID_SIZE // 2
        y = y_idx * GRID_SIZE + GRID_SIZE // 2
        self.position = (x, y)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывает объект змейка"""

    def __init__(self, body_color):
        super().__init__(body_color)
        self.length = 1
        self.next_direction = None
        self.body_color = SNAKE_COLOR
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
        """Движение змейки"""
        head = self.get_head_position()
        x, y = head  # Запомнили в переменные координаты головы змейки

        # Смена координат в зависимости от направления
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

        # Применяем цикл единожды для любого случая
        new_pos = (new_pos[0] % SCREEN_WIDTH, new_pos[1] % SCREEN_HEIGHT)
        self.positions.insert(0, new_pos)

        # Удаляем хвост, если длина списка больше текущей длины змейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отображаем экземпляр в игре"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
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
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    handle_keys(snake)
    while True:
        clock.tick(SPEED)
        screen.fill((0, 0, 0))
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()
        pygame.display.update()
        # Увеличиваем хвост, когда сьели яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
        if snake.get_head_position() in snake.position[1:]:
            return False


if __name__ == '__main__':
    main()

# Функция обработки действий пользователя
