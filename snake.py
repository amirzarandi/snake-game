import pygame
from pygame import color
import random
import time

pygame.init()

# Custom Variables
message_font = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 15)
score_color = (255, 255, 102)
snake_color = (0, 0, 0)
message_color = (213, 50, 80)
food_color = (0, 255, 0)
bg_color = (50, 153, 213)
dis_width = 600
dis_height = 400
snake_block = 10
snake_speed = 15

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake game by Amir')

clock = pygame.time.Clock()


def High_score(score, high_score):
    value = score_font.render(
        "High Score: " + str(max(score, high_score)), True, score_color)
    dis.blit(value, [200, 0])


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, score_color)
    dis.blit(value, [0, 0])


def our_snake(snake_color, snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snake_color, [
                         x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = message_font.render(msg, True, color)
    dis.blit(mesg, [(dis_width/2 - len(msg)*4.25), dis_height/3])


def gameLoop():
    game_close = False
    game_over = False

    # Initial Snake
    x1 = dis_width/2
    y1 = dis_height/2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1

    # Initial Food
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_close:

        # Game Over Screen
        while game_over:
            dis.fill(bg_color)
            x1_change = 0
            y1_change = 0
            time.sleep(1)
            our_snake(bg_color, snake_block, snake_List)
            message("You Lost! Press Q-Quit or C-Play Again", message_color)
            pygame.display.update()

            # Register Game Over Screen Controls
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = True
                        game_over = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Register Game Controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Snake Hits the Wall
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over = True

        # Snake Movement
        x1 += x1_change
        y1 += y1_change

        dis.fill(bg_color)

        pygame.draw.rect(dis, food_color, [
                         foodx, foody, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        # Setting the Snake Length
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Snake Bites Its Tail
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over = True

        our_snake(snake_color, snake_block, snake_List)

        # Displaying Scores
        Your_score(Length_of_snake - 1)
        log = open("snake_log.txt", "r")
        hs = int(log.read())
        High_score(Length_of_snake - 1, hs)

        # Regisitering A New High Score
        if Length_of_snake - 1 > hs:
            log = open("snake_log.txt", "w")
            log.write(str(Length_of_snake - 1))

        pygame.display.update()

        # Snake Eats a Food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(
                0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(
                0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
