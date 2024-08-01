# pong_game.py
import pygame
import random

# Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
White = (255, 255, 255)
Black = (0, 0, 0)

# Ball properties
Ballsize = 10
ball_speed_x = 4
ball_speed_y = 4

# Paddle properties
paddle_width = 10
paddle_height = 100
paddle_speed = 6

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Ball initial position and speed
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = ball_speed_x
ball_speed_y = ball_speed_y

# Paddles initial position
paddle1Pos = (HEIGHT - paddle_height) // 2
paddle2Pos = (HEIGHT - paddle_height) // 2

# Scores
Score1 = 0
Score2 = 0

# Font for displaying the score
font4Score = pygame.font.Font(None, 36)

# Game loop
game = True
while game:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Move paddles
    if keys[pygame.K_w] and paddle1Pos > 0:
        paddle1Pos -= paddle_speed
    if keys[pygame.K_s] and paddle1Pos < HEIGHT - paddle_height:
        paddle1Pos += paddle_speed
    if keys[pygame.K_UP] and paddle2Pos > 0:
        paddle2Pos -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2Pos < HEIGHT - paddle_height:
        paddle2Pos += paddle_speed

    # Move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top and bottom
    if ball_y <= 0 or ball_y >= HEIGHT - Ballsize:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddles
    if (ball_x <= paddle_width and paddle1Pos < ball_y < paddle1Pos + paddle_height) or (
            ball_x >= WIDTH - paddle_width - Ballsize and paddle2Pos < ball_y < paddle2Pos + paddle_height):
        ball_speed_x = -ball_speed_x

    # Ball out of bounds
    if ball_x < 0:
        Score2 += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_speed_x = ball_speed_x * random.choice([1, -1])
        ball_speed_y = ball_speed_y * random.choice([1, -1])
    elif ball_x > WIDTH:
        Score1 += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_speed_x = ball_speed_x * random.choice([1, -1])
        ball_speed_y = ball_speed_y * random.choice([1, -1])

    # Clear screen
    screen.fill(Black)

    # Draw ball
    pygame.draw.circle(screen, White, (ball_x, ball_y),Ballsize)

    # Draw paddles
    pygame.draw.rect(screen, White, (0, paddle1Pos, paddle_width, paddle_height))
    pygame.draw.rect(screen, White, (WIDTH - paddle_width, paddle2Pos, paddle_width, paddle_height))

    # Draw score
    score_text = font4Score.render(f"{Score1} - {Score2}", True, White)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # Update screen
    pygame.display.flip()

    # game's speed
    pygame.time.delay(16)

# Quit Pygame
pygame.quit()
