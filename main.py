import pygame
import random
import sys
import os

pygame.init()

# Размеры экрана
width = 700
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zmeika")

# Цвета
snake_color = (255, 255, 255)
apple_color = (128, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (128, 0, 0)

# Шрифты
score_font = pygame.font.SysFont("Arial", 20)
game_clock = pygame.time.Clock()

# Путь к файлу с рекордами
record_file = "records.txt"


# Классы для экрана и кнопки
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)  # кнопка красная
        text_surface = pygame.font.Font(None, 40).render(self.text, True, WHITE)  # текст кнопки белый
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.action:
            self.action()


# Чтение рекордов
def read_records():
    if not os.path.exists(record_file):
        return 0
    with open(record_file, 'r') as file:
        return int(file.read().strip())


# Сохранение рекордов
def save_record(score):
    current_record = read_records()
    if score > current_record:
        with open(record_file, 'w') as file:
            file.write(str(score))


# Начальный экран
def start_screen():
    screen.fill(BLACK)  # фон черный

    title = pygame.font.Font(None, 60).render('Zmeika', True, RED)  # цвет текста красный
    title_rect = title.get_rect(center=(width // 2, height // 3))
    screen.blit(title, title_rect)

    start_button = Button('Начать игру', width // 4, height // 2, width // 2, 50, start_game)
    start_button.draw(screen)

    records_button = Button('Рекорды', width // 4, height // 1.6, width // 2, 50, show_records)
    records_button.draw(screen)

    pygame.display.update()

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_hovered(event.pos):
                    start_button.click()
                    waiting_for_click = False
                elif records_button.is_hovered(event.pos):
                    records_button.click()
                    waiting_for_click = False


# Экран завершения игры
def game_over_screen(score):
    screen.fill(BLACK)  # фон черный

    game_over_text = pygame.font.Font(None, 60).render('Игра окончена!', True, RED)  # текст красный
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 3))
    screen.blit(game_over_text, game_over_rect)

    score_text = score_font.render(f"Съедено яблок: {score}", True, WHITE)  # текст белый
    score_rect = score_text.get_rect(center=(width // 2, height // 2))
    screen.blit(score_text, score_rect)

    # Сохраняем рекорд
    save_record(score)

    pygame.display.update()
    pygame.time.wait(2000)


# Экран с рекордами
def show_records():
    screen.fill(BLACK)

    title = pygame.font.Font(None, 60).render('Рекорды', True, RED)  # текст красный
    title_rect = title.get_rect(center=(width // 2, height // 4))
    screen.blit(title, title_rect)

    current_record = read_records()
    record_text = score_font.render(f"Рекорд: {current_record} съеденных яблок", True, WHITE)  # текст белый
    record_rect = record_text.get_rect(center=(width // 2, height // 2))
    screen.blit(record_text, record_rect)

    back_button = Button('Назад', width // 4, height // 1.5, width // 2, 50, start_screen)
    back_button.draw(screen)

    pygame.display.update()

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_hovered(event.pos):
                    back_button.click()
                    waiting_for_click = False


# Логика игры
def start_game():
    block_size = 20
    speed = 10
    snake_length = 3
    snake_segments = []

    for i in range(snake_length):
        snake_segments.append(pygame.Rect((width / 2) - (block_size * i), height / 2, block_size, block_size))

    snake_move = "right"
    next_move = "right"
    apple_pos = pygame.Rect(random.randint(0, width - block_size), random.randint(0, height - block_size), block_size,
                            block_size)

    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_move != "down":
                    next_move = "up"
                elif event.key == pygame.K_DOWN and snake_move != "up":
                    next_move = "down"
                elif event.key == pygame.K_LEFT and snake_move != "right":
                    next_move = "left"
                elif event.key == pygame.K_RIGHT and snake_move != "left":
                    next_move = "right"

        # Обновление направления
        snake_move = next_move

        # Движение змейки
        if snake_move == "up":
            snake_segments.insert(0, pygame.Rect(snake_segments[0].left, snake_segments[0].top - block_size, block_size,
                                                 block_size))
        elif snake_move == "down":
            snake_segments.insert(0, pygame.Rect(snake_segments[0].left, snake_segments[0].top + block_size, block_size,
                                                 block_size))
        elif snake_move == "left":
            snake_segments.insert(0, pygame.Rect(snake_segments[0].left - block_size, snake_segments[0].top, block_size,
                                                 block_size))
        elif snake_move == "right":
            snake_segments.insert(0, pygame.Rect(snake_segments[0].left + block_size, snake_segments[0].top, block_size,
                                                 block_size))

        # Яблоко съедено
        if snake_segments[0].colliderect(apple_pos):
            apple_pos = pygame.Rect(random.randint(0, width - block_size), random.randint(0, height - block_size),
                                    block_size, block_size)
            snake_length += 1
            score += 1

        # Обрезка хвоста змейки
        if len(snake_segments) > snake_length:
            snake_segments.pop()

        # Столкновение со стеной
        if snake_segments[0].left < 0 or snake_segments[0].right > width or snake_segments[0].top < 0 or snake_segments[
            0].bottom > height:
            game_over = True

        # Столкновение с телом змейки
        for segment in range(1, len(snake_segments)):
            if snake_segments[0].colliderect(snake_segments[segment]):
                game_over = True

        # Очистка экрана
        screen.fill(BLACK)

        # Отображение змейки
        for idx, segment in enumerate(snake_segments):
            if idx == 0:
                pygame.draw.circle(screen, snake_color, segment.center, block_size / 2)
            else:
                pygame.draw.circle(screen, snake_color, segment.center, block_size / 2)
                pygame.draw.circle(screen, (148, 0, 211), segment.center, block_size / 4)

        # Отображение яблока
        pygame.draw.circle(screen, apple_color, apple_pos.center, block_size / 2)

        # Отображение счета
        score_text = score_font.render(f"Съедено яблок: {score}", True, WHITE)  # текст белый
        screen.blit(score_text, (10, 10))

        pygame.display.update()

        # Контроль за частотой кадров
        game_clock.tick(speed)

    # Экран завершения игры
    game_over_screen(score)
    start_screen()


# Главный цикл программы
if __name__ == "__main__":
    start_screen()
