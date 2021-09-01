import pygame
import os
import random

SCREEN_W, SCREEN_H = 450, 720
PIPE_IMG = pygame.transform.scale2x(pygame.image.load('imgs/pipe.png'))
FLOOR_IMG = pygame.transform.scale2x(pygame.image.load('imgs/base.png'))
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load('imgs/bg.png'))
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load('imgs/bird1.png')),
             pygame.transform.scale2x(pygame.image.load('imgs/bird2.png')),
             pygame.transform.scale2x(pygame.image.load('imgs/bird3.png'))]

pygame.font.init()
POINTS_FONT = pygame.font.SysFont('arial', 50)

class Bird:
    IMGS = BIRD_IMGS
    #rotation animation
    MAX_ROTATION = 25
    ROTATION_SPEED = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_counter = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        #calculate the movement (deslocamento)
        self.time += 1
        movement = 1.5 * (self.time**2) + self.speed * self.time
        #constrain the movement
        if movement > 16:
            movement = 16
        elif movement < 0:
            movement-=2

        self.y += movement
        #bird angle
        if movement<0 or self.y < (self.height+50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED

    def draw(self, screen):
        #define which image to use
        self.image_counter += 1

        if self.image_counter < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_counter < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        elif self.image_counter < self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        elif self.image_counter < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        elif self.image_counter >= self.ANIMATION_TIME*4+1:
            self.image = self.IMGS[0]
            self.image_counter = 0

        #if the bird is falling, don't move the wings
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.image_counter = self.ANIMATION_TIME*2

        #draw image
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        image_center = self.image.get_rect(topleft=(self.x,self.y)).center
        rectangle = rotated_image.get_rect(center=image_center)
        screen.blit(rotated_image, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_bottom = 0
        self.top_pipe = pygame.transform.flip(PIPE_IMG, False, True)
        self.bottom_pipe = PIPE_IMG
        self.passed = False
        self.define_height()

    def define_height(self):
        self.height = random.randrange(50, SCREEN_H-350)
        self.pos_top = self.height - self.top_pipe.get_height()
        self.pos_bottom = self.height + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.top_pipe, (self.x, self.pos_top))
        screen.blit(self.bottom_pipe, (self.x, self.pos_bottom))

    def collision(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe)

        top_distance = (self.x - bird.x, self.pos_top - round(bird.y))
        bottom_distance = (self.x - bird.x, self.pos_bottom - round(bird.y))

        collision_top = bird_mask.overlap(top_mask, top_distance)
        collision_bottom = bird_mask.overlap(bottom_mask, bottom_distance)

        if collision_top or collision_bottom:
            return True
        else:
            return False

class Floor:
    SPEED = 5
    WIDTH = FLOOR_IMG.get_width()
    IMAGE = FLOOR_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))


def draw_screen(screen, birds, pipes, floor, points):
    screen.blit(BACKGROUND_IMG, (0, 0))

    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    text = POINTS_FONT.render(f"Score: {points}", 1, (230,230,230))
    screen.blit(text, (SCREEN_W-10-text.get_width(), 10))
    floor.draw(screen)
    pygame.display.update()

def main():
    birds = [Bird(230, 350)]
    floor = Floor(SCREEN_H-70)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    points = 0
    clock = pygame.time.Clock()

    playing = True
    while playing:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        for bird in birds:
            bird.move()
        floor.move()

        add_pipe = False
        pipes_to_remove = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collision(bird):
                    birds.pop(i)
                    #main()
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()
            if pipe.x + pipe.top_pipe.get_width() < 0:
                pipes_to_remove.append(pipe)

        if add_pipe:
            points += 1
            pipes.append(Pipe(600))
        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height())>floor.y or bird.y < 0:
                birds.pop(i)
                #main()

        draw_screen(screen, birds, pipes, floor, points)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
