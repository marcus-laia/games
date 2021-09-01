import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', ('x', 'y'))
BLOCK_SIZE = 20
SPEED = 20

#rbg colors
WHITE = (255,255,255)
RED = (200,0,0)
BLUE = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

class SnakeGame():

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        #init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        #init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-2*BLOCK_SIZE, self.head.y)]
        self.score = 0
        self.food = None
        self.place_food()

    def place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def play_step(self):
        # Collect User Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        # Move
        self.move(self.direction) #update the head
        self.snake.insert(0, self.head)

        # Check if game over
        game_over = False
        if self.collision():
            game_over = True
            return game_over, self.score

        # Place new food or just move
        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

        # Update ui and clod
        self.update_ui()
        self.clock.tick(SPEED)
        # Return game over and score

        return game_over, self.score

    def collision(self):
        #hits boundary
        if self.head.x > self.w-BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h-BLOCK_SIZE or self.head.y < 0:
            return True

        #hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, BLOCK_SIZE-8, BLOCK_SIZE-8))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()

    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if direction == Direction.LEFT:
            x -= BLOCK_SIZE
        if direction == Direction.UP:
            y -= BLOCK_SIZE
        if direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    #game loop
    while True:
        game_over, score = game.play_step()


        #break if game over
        if game_over:
            print('Final Score:', score)
            break

    pygame.quit()
