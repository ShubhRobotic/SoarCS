import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Snake and fruit settings
snake_block = 20
snake_speed = 15

# Font
font_style = pygame.font.SysFont(None, 35)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [width / 6, height / 3])

def draw_border():
    pygame.draw.rect(window, blue, [0, 0, width, height], 5)

def display_score(score):
    score_text = font_style.render(f"Score: {score}", True, white)
    window.blit(score_text, [10, 10])

def display_time(start_time):
    elapsed_time = int(time.time() - start_time)
    time_text = font_style.render(f"Time: {elapsed_time} s", True, white)
    window.blit(time_text, [width - 120, 10])

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    fruitx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    fruity = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    clock = pygame.time.Clock()
    start_time = time.time()

    while not game_over:

        while game_close == True:
            window.fill(black)
            draw_border()
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_d and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_w and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_s and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width - snake_block or x1 < 0 or y1 >= height - snake_block or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        window.fill(black)
        draw_border()
        pygame.draw.rect(window, red, [fruitx, fruity, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for segment in snake_List:
            pygame.draw.rect(window, green, [segment[0], segment[1], snake_block, snake_block])

        display_score(Length_of_snake - 1)
        display_time(start_time)

        pygame.display.update()

        if x1 == fruitx and y1 == fruity:
            fruitx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            fruity = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
