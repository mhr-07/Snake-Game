import pygame
import sys
import random
import os

# Initializing Pygame
pygame.init()
pygame.mixer.init()

# Screen size
WIDTH, HEIGHT = 650, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Font and clock
font = pygame.font.SysFont('consolas', 28)
clock = pygame.time.Clock()

# Load sounds
eat_sound = pygame.mixer.Sound("eat.mp3")
collision_sound = pygame.mixer.Sound("collision.mp3")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)
RED = (237, 28, 36)
BLUE = (0, 162, 232)
HOVER_COLOR = (50, 200, 50)
IDLE_COLOR = (0, 100, 200)

# Game settings
SNAKE_BLOCK = 24
FOOD_BLOCK = 18
HIGH_SCORE_FILE = "highscore.txt"

# Create high score file if it doesn't exist
if not os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write("0")

# Button class
class Button:
    def __init__(self, text, x, y, action):
        self.text = text
        self.rect = pygame.Rect(x, y, 240, 50)
        self.action = action

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else IDLE_COLOR

        pygame.draw.rect(win, color, self.rect, border_radius=10)

        label = font.render(self.text, True, WHITE)     # true is anti-aliasing used to smooth the edges and make it look better
        win.blit(label, (self.rect.x + (240 - label.get_width()) // 2, self.rect.y + 10))

        if self.rect.collidepoint(mouse_pos) and mouse_click:
            pygame.time.delay(200)
            self.action()

# Draw the snake
def draw_snake(snake):
    for i, block in enumerate(snake):
        color = GREEN if i == 0 else (0, 120 + i * 2 % 100, 0)
        pygame.draw.rect(win, color, (*block, SNAKE_BLOCK, SNAKE_BLOCK), border_radius=5)

        # Draw the eyes of the snake head
        if i == 0:
            for dx in (6, SNAKE_BLOCK - 6):
                pygame.draw.circle(win, BLACK, (block[0] + dx, block[1] + 6), 3)

# Run the snake game
def snake_game():
    snake = [(100, 50) ,(76, 50)]
    direction = (SNAKE_BLOCK, 0)

    def random_food():
        return (
            random.randint(0, (WIDTH - FOOD_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK + (SNAKE_BLOCK - FOOD_BLOCK) // 2,
            random.randint(0, (HEIGHT - FOOD_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK + (SNAKE_BLOCK - FOOD_BLOCK) // 2
        )

    food_pos = random_food()
    score = 0

    while True:
        clock.tick(8)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction[1] == 0:
                    direction = (0, -SNAKE_BLOCK)
                elif event.key == pygame.K_DOWN and direction[1] == 0:
                    direction = (0, SNAKE_BLOCK)
                elif event.key == pygame.K_LEFT and direction[0] == 0:
                    direction = (-SNAKE_BLOCK, 0)
                elif event.key == pygame.K_RIGHT and direction[0] == 0:
                    direction = (SNAKE_BLOCK, 0)

        # Move snake
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Collision with self or wall
        if head in snake or not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            update_high_score(score)
            collision_sound.play()
            pygame.time.delay(1500)
            break

        snake.insert(0, head)

        # Check food collision
        if abs(head[0] - food_pos[0]) < FOOD_BLOCK and abs(head[1] - food_pos[1]) < FOOD_BLOCK:
            eat_sound.play()
            score += 1
            food_pos = random_food()
        else:
            snake.pop()

        # Draw everything
        win.fill(WHITE)
        draw_snake(snake)
        pygame.draw.rect(win, RED, (*food_pos, FOOD_BLOCK, FOOD_BLOCK), border_radius=3)
        score_text = font.render(f"Score: {score}", True, BLACK)
        win.blit(score_text, (10, 10))
        pygame.display.update()

    main_menu()

# Update high score in file
def update_high_score(new_score):
    with open(HIGH_SCORE_FILE) as f:
        current_high = int(f.read())
    if new_score > current_high:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(new_score))

# Show high score screen
def show_high_score():
    with open(HIGH_SCORE_FILE) as f:
        score = f.read()

    win.fill(WHITE)
    win.blit(font.render("High Score", True, BLUE), (WIDTH // 2 - 80, HEIGHT // 3))
    win.blit(font.render(score, True, GREEN), (WIDTH // 2 - 20, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    main_menu()

# Quit the game
def quit_game():
    pygame.quit()
    sys.exit()

# Main menu
def main_menu():
    buttons = [
        Button("New Game", WIDTH // 2 - 120, 140, snake_game),
        Button("High Score", WIDTH // 2 - 120, 210, show_high_score),
        Button("Exit", WIDTH // 2 - 120, 280, quit_game)
    ]

    while True:
        win.fill(WHITE)
        win.blit(font.render("Snake Game", True, BLACK), (WIDTH // 2 - 100, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        for btn in buttons:
            btn.draw()

        pygame.display.update()
        clock.tick(60)

# Start the game
main_menu()
