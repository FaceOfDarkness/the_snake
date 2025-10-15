import pygame
import random

# Константы игрового поля и цветов
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        if position is None:
            self.position = (0, 0)
        else:
            self.position = position
        self.body_color = body_color


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        super().__init__((start_x, start_y), body_color=SNAKE_COLOR)
        self.positions = [(start_x, start_y)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction
        self.body_color = SNAKE_COLOR

    def handle_keys(self):
        """Обработка нажатий клавиш для смены направления."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT

    def update_direction(self):
        """Обновление текущего направления движений."""
        self.direction = self.next_direction

    def move(self):
        """Перемещение змейки."""
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)
        self.positions = [new_head] + self.positions[:-1]

    def grow(self):
        """Увеличение длины змейки после съедания яблока."""
        self.positions.append(self.positions[-1])

    def check_collision(self):
        """Проверка столкновений со стенами и собой."""
        head = self.positions[0]
        if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
            return True
        if head in self.positions[1:]:
            return True
        return False

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс состояния змейки в начальную."""
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.positions = [(start_x, start_y)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction

    def draw(self, surface):
        """Отрисовка змейки."""
        for pos in self.positions:
            rect = pygame.Rect(
                pos[0] * GRID_SIZE,
                pos[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Генерация начальной позиции яблока."""
        position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        super().__init__(position, body_color=APPLE_COLOR)
        self.body_color = APPLE_COLOR

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)

    def randomize_position(self, snake_positions):
        """Генерация новой позиции яблока, избегая координаты змейки."""
        while True:
            position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if position not in snake_positions:
                self.position = position
                break


def handle_keys(snake):
    """Обработка событий клавиш для змейки."""
    snake.handle_keys()


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.check_collision():
            pygame.quit()
            raise SystemExit

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
