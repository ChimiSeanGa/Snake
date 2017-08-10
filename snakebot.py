import sys
import time
import pygame
from collections import deque
import random

class Body:
    def __init__(self, x, y):
        self.headX = x
        self.headY = y
        self.tailX = x-1
        self.tailY = y

# directions
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# set width and height of each grid block
WIDTH = 19
HEIGHT = 19

# set margin of grid blocks
MARGIN = 1

def game():
    # initialize pygame
    pygame.init()
    pygame.font.init()

    #set screen dimensions
    screen = pygame.display.set_mode([401, 401])

    # set game loop terminator to false
    done = False
    quit = False

    # initialize snake
    snake = Body(10, 10)

    direction = RIGHT
    draw = 0

    # create grid
    screen.fill(BLACK)
    color = WHITE
    for row in range(20):
        for column in range(20):
            pygame.draw.rect(screen, color, [(MARGIN+WIDTH) * column + MARGIN,
                                                        (MARGIN+HEIGHT) * row + MARGIN,
                                                        WIDTH,
                                                        HEIGHT])

    pygame.display.update()

    body = []
    dirqueue = deque([0])

    count = 0

    objectx = random.randint(0, 19)
    objecty = random.randint(0, 19)
    ate = False

    clock = pygame.time.Clock()

    # game loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # smart snake
        if snake.headX != 0:
            if snake.headY % 2 == 0:
                if snake.headX == 19:
                    direction = DOWN
                else:
                    direction = RIGHT
            else:
                if snake.headX == 1:
                    if snake.headY == 19:
                        direction = LEFT
                    else:
                        direction = DOWN
                else:
                    direction = LEFT
        else:
            if snake.headY == 0:
                direction = RIGHT
            else:
                direction = UP

        print("(" + str(snake.headX) + ", " + str(snake.headY) + ") " + str(direction))

        # end smart snake

        dirqueue.appendleft(direction)

        body.append((snake.headX, snake.headY))

        if direction == RIGHT:
            snake.headX += 1
        elif direction == UP:
            snake.headY -= 1
        elif direction == LEFT:
            snake.headX -= 1
        elif direction == DOWN:
            snake.headY += 1

        if snake.headX == objectx and snake.headY == objecty:
            ate = True

        if ate:
            dirqueue.append(-1)
            dirqueue.append(-1)
            dirqueue.append(-1)
            dirqueue.append(-1)

            objectx = random.randint(0, 19)
            objecty = random.randint(0, 19)

            while (objectx, objecty) in body:
                objectx = random.randint(0, 19)
                objecty = random.randint(0, 19)

            ate = False

        if count > 1:
            body.remove((snake.tailX, snake.tailY))

        if count > 0:
            tailDir = dirqueue.pop()
            if tailDir == RIGHT:
                snake.tailX += 1
            elif tailDir == UP:
                snake.tailY -= 1
            elif tailDir == LEFT:
                snake.tailX -= 1
            elif tailDir == DOWN:
                snake.tailY += 1
            else:
                body.append((snake.tailX, snake.tailY))

        count += 1

        if (snake.headX < 0 or snake.headX > 19 or snake.headY < 0
            or snake.headY > 19 or (snake.headX, snake.headY) in body):
            done = True
            continue

        color = GREEN

        pygame.draw.rect(screen, color, [(MARGIN+WIDTH) * snake.headX + MARGIN,
                                                    (MARGIN+HEIGHT) * snake.headY + MARGIN,
                                                    WIDTH,
                                                    HEIGHT])

        color = WHITE

        pygame.draw.rect(screen, color, [(MARGIN+WIDTH) * snake.tailX + MARGIN,
                                                    (MARGIN+HEIGHT) * snake.tailY + MARGIN,
                                                    WIDTH,
                                                    HEIGHT])

        color = RED

        pygame.draw.rect(screen, color, [(MARGIN+WIDTH) * objectx + MARGIN,
                                                    (MARGIN+HEIGHT) * objecty + MARGIN,
                                                    WIDTH,
                                                    HEIGHT])

        pygame.display.update()

        clock.tick(60)
        # time.sleep(0.02)

    pygame.draw.rect(screen, WHITE, [101, 101, 199, 199])

    myfont = pygame.font.SysFont(None, 50)
    label = myfont.render("Game over", 1, (0, 0, 0))
    screen.blit(label, (110, 180))
    pygame.display.update()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

    pygame.quit()
    return False

def main():
    while game():
        continue

if __name__ == "__main__":
    main()
