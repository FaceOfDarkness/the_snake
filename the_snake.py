import pygame
import random

# Размеры окна
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость
SPEED = 10

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class Snake:
    """Класс змейки"""
    def __init__(self):
        """Инициализация змейки"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction
        self.alive = True

    def handle_keys(self):
        """Обработка нажатий клавиш"""
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
        """Обновление направления движения"""
        self.direction = self.next_direction

    def move(self):
        """Движение змейки и проверка столкновений"""
        self.update_direction()
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        # Обертка по горизонтали
        if new_head[0] < 0:
            new_head = (GRID_WIDTH - 1, new_head[1])
        elif new_head[0] >= GRID_WIDTH:
            new_head = (0, new_head[1])

        # Обертка по вертикали
        if new_head[1] < 0:
            new_head = (new_head[0], GRID_HEIGHT - 1)
        elif new_head[1] >= GRID_HEIGHT:
            new_head = (new_head[0], 0)

        # Проверка столкновения с самим собой
        if new_head in self.positions:
            self.alive = False
            return

        # Обновление позиций
        self.positions = [new_head] + self.positions[:-1]

    def grow(self):
        """Увеличение длины змейки"""
        self.positions.append(self.positions[-1])

    def draw(self, surface):
        """Отображение змейки"""
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE,
                               GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, SNAKE_COLOR, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple:
    """Класс яблока"""
    def __init__(self, snake_positions):
        """Инициализация яблока"""
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        """Генерация случайной позиции для яблока"""
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1),
                   random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_positions:
                return pos

    def respawn(self, snake_positions):
        """Переигрывание яблока в новое место"""
        self.position = self.random_position(snake_positions)

    def draw(self, surface):
        """Отображение яблока"""
        rect = pygame.Rect(self.position[0] * GRID_SIZE,
                           self.position[1] * GRID_SIZE,
                           GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, APPLE_COLOR, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def main():
    """Главная функция игры"""
    snake = Snake()
    apple = Apple(snake.positions)
    score = 0

    while True:
        clock.tick(SPEED)
        snake.handle_keys()
        snake.move()

        if not snake.alive:
            break  # Игра окончена

        if snake.positions[0] == apple.position:
            snake.grow()
            score += 1
            apple.respawn(snake.positions)

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        # Отображение счета
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Очки: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    # Конец игры
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Игра окончена!", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                   SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == '__main__':
    main()
