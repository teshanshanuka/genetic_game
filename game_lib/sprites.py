import pygame
import numpy as np
from typing import Union, List

import game_lib.ann as ann
from pygame.sprite import Sprite, Group


class Mushroom(Sprite):
    """    Mushroom    """
    id = 0

    def __init__(self, image, resize_to, Y, resolution, released=False):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), resize_to)
        self.sizeX = pygame.Surface.get_width(self.image)
        self.sizeY = pygame.Surface.get_height(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (resolution[0], Y)
        self.velocity = 0

        self.resolution = resolution
        self.reset_pos()
        self.released = released

        self.id = Mushroom.id
        Mushroom.id += 1

    def __repr__(self):
        return "{}_{}".format(self.__class__.__name__, self.id)

    def reset_pos(self):
        self.velocity = np.random.randint(15, 20)
        self.rect.x = self.resolution[0]
        self.released = False

    def update(self):
        if not self.released:
            return
        new_x = self.rect.x - self.velocity
        if new_x > 0:
            self.rect.x = new_x
        else:
            self.reset_pos()


class Fireball(Sprite):
    """    Fireball    """
    id = 0

    def __init__(self, image, resize_to, Y, resolution, released=False):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), resize_to)
        self.sizeX = pygame.Surface.get_width(self.image)
        self.sizeY = pygame.Surface.get_height(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (resolution[0], Y)
        self.velocity = 0

        self.resolution = resolution
        self.reset_pos()
        self.released = released

        self.id = Fireball.id
        Fireball.id += 1

    def __repr__(self):
        return "{}_{}".format(self.__class__.__name__, self.id)

    def reset_pos(self):
        self.velocity = np.random.randint(15, 20)
        self.rect.x = self.resolution[0]
        self.released = False

    def update(self):
        if not self.released:
            return
        new_x = self.rect.x - self.velocity
        if new_x > 0:
            self.rect.x = new_x
        else:
            self.reset_pos()


class ObstacleGroup(Group):
    def __init__(self, release_count, release_dist):
        super().__init__()
        self.release_count = release_count
        self.release_dist = release_dist

    def update(self, *args):
        sprites = self.sprites()
        farthest = None
        released = 0
        for sprite in sprites:
            if sprite.released:
                # print("released:", sprite)
                released += 1
                if not farthest or farthest.rect.x < sprite.rect.x:
                    farthest = sprite

        if released == 0:
            sprites[np.random.randint(0, len(sprites))].released = True
            # for sprite in sprites:
            #     print(sprite, ":", sprite.released)
            # print("started")
        elif farthest and farthest.rect.x < self.release_dist:
            while released < self.release_count:
                idx = np.random.randint(0, len(sprites))
                if not sprites[idx].released:
                    sprites[idx].released = True
                    released += 1

        super().update(*args)

    def reset_pos(self):
        for sprite in self.sprites():
            sprite.reset_pos()


class Mario(Sprite):
    """    Mario!    """
    id = 0

    def __init__(self, image, resize_to, ducked_image, ducked_resize_to, X, Y, resolution, horizontal_step, jump_vel,
                 gravity, max_fail_count, gene=None):
        super().__init__()
        self.image1 = pygame.transform.scale(pygame.image.load(image), resize_to)
        self.image2 = pygame.transform.scale(pygame.image.load(ducked_image), ducked_resize_to)
        self.image = self.image1
        self.sizeX = pygame.Surface.get_width(self.image)
        self.sizeY = pygame.Surface.get_height(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (X, Y)
        self.init_Y = Y

        self.sizeX1 = pygame.Surface.get_width(self.image1)
        self.sizeY1 = pygame.Surface.get_height(self.image1)
        self.rect1 = self.image1.get_rect()
        self.sizeX2 = pygame.Surface.get_width(self.image2)
        self.sizeY2 = pygame.Surface.get_height(self.image2)
        self.rect2 = self.image2.get_rect()
        self.ydiff = self.sizeY1 - self.sizeY2

        self.resolution = resolution
        self.horizontal_step = horizontal_step
        self.jump_vel = jump_vel
        self.gravity = gravity
        self.is_jumping = False
        self.is_ducked = False
        self.is_going_fw = False
        self.is_going_bw = False
        self.t_jump = 0
        self.bogus = (
            (np.random.randint(-35, 45), np.random.randint(75, 85)),
            (np.random.randint(-5, 5), np.random.randint(95, 105)))

        self.id = Mario.id
        Mario.id += 1
        self.score = 0
        self.game_over = False
        self.fail_count = 0
        self.max_fail_count = max_fail_count
        self.finished = False
        self.last_action = "reset"
        self.fitness = 0

        self.model = None

        self.init_nn(gene)

    def __repr__(self):
        return "{}_{}".format(self.__class__.__name__, self.id)

    def reset_pos(self):
        print(self, "failed:", self.fail_count, "score:", self.score)
        x, _ = self.rect.topleft
        self.image = self.image1
        self.sizeX = self.sizeX1
        self.sizeY = self.sizeY1
        self.rect = self.rect1
        self.rect.topleft = (x, self.init_Y)
        self.fail_count += 1

    def update(self, arg):
        if self.fail_count >= self.max_fail_count:
            if not self.finished:
                print(self, "is finished. score:", self.fitness)
                self.finished = True
            return
        if self.game_over:
            self.reset_pos()
            self.fitness = self.score
            self.score = 0
            self.back_propagate_nn(arg)
            self.game_over = False
            return

        # ugly if. please ignore
        if isinstance(arg, str):
            state = arg
        else:
            state = self.play(arg)

        if state == "duck" and not self.is_ducked:
            x, y = self.rect.topleft
            self.image = self.image2
            self.sizeX = self.sizeX2
            self.sizeY = self.sizeY2
            self.rect = self.rect2
            self.rect.topleft = (x, y + self.ydiff)
            self.is_ducked = True

        elif state == "jump" and not self.is_ducked:  # can't jump if ducked
            self.is_jumping = True
        elif state == "reset" and self.is_ducked:
            x, y = self.rect.topleft
            self.image = self.image1
            self.sizeX = self.sizeX1
            self.sizeY = self.sizeY1
            self.rect = self.rect1
            self.rect.topleft = (x, y - self.ydiff)
            self.is_ducked = False

        if self.is_jumping:
            new_y = self.init_Y - (self.jump_vel * self.t_jump - 0.5 * self.gravity * self.t_jump ** 2)
            if new_y > self.init_Y:
                self.rect.y = self.init_Y
                self.t_jump = 0
                self.is_jumping = False
            else:
                self.rect.y = new_y
                self.t_jump += 1

        self.score += 1

    def play(self, obstacles) -> str:
        return self.nn(obstacles)

    # def bogus_nn(self, obstacles: List[Union[Mushroom, Fireball]]):
    #     state = ""
    #     for obstacle in obstacles:
    #         if not obstacle.released:
    #             continue
    #
    #         if isinstance(obstacle, Fireball):
    #             if self.bogus[0][0] < (obstacle.rect.x - self.rect.x) < self.bogus[0][1]:
    #                 state = "duck"
    #         else:  # a mushroom
    #             if self.bogus[1][0] < (obstacle.rect.x - self.rect.x) < self.bogus[1][1]:
    #                 state = "jump"
    #         if not state:
    #             state = "reset"
    #
    #     self.last_action = state
    #     return state

    def respawn(self, gene):
        self.fail_count = 0
        self.finished = False
        self.init_nn(gene)

    # TODO: From here onwards

    def init_nn(self, gene):
        # initialize the neural network
        # set initial weights from the gene
        self.model, self.layer1, self.out_layer = ann.init_ann(gene)

    def nn(self, obstacles: List[Union[Mushroom, Fireball]]):
        # return state using inputs obstacle.rect.x, obstacle.rect.y, obstacle.velocity
        input_ = []
        for obstacle in obstacles:
            input_.extend([obstacle.rect.x, obstacle.rect.y, obstacle.velocity])

        x = np.reshape(np.array(input_), (1, 12))
        y_prediction = ann.predict(self.model, x)

        index = np.argmax(y_prediction)
        # return the output of the ann as a string: 'jump'.
        if index == 0:
            y = 'jump'
        elif index == 1:
            y = 'duck'
        else:
            y = 'reset'

        self.last_action = y
        return y

    def back_propagate_nn(self, obstacles: List[Union[Mushroom, Fireball]]):
        # update weights of the NN
        # self.last_action contains last action ["jump","duck","reset"]
        # calculate error and update the NN upon that

        input_ = []
        for obstacle in obstacles:
            input_.extend([obstacle.rect.x, obstacle.rect.y, obstacle.velocity])

        x = np.reshape(np.array(input_), (1, 12))

        if self.last_action == 'reset':
            # x = np.array([0,0,1],dtype='float32')
            # y = choice(['jump','duck']) shape (1,3)
            # y = choice([[0,1,0],[1,0,0]])
            y = [1, 1, 0]
            y = np.array(y, dtype='float32')

        elif self.last_action == 'duck':
            # x = np.array([0,1,0],dtype='float32')
            # y = choice(['jump','reset'])
            # y = choice([[1,0,0],[0,0,1]])
            y = [1, 0, 1]
        else:
            # x = np.array([1,0,0],dtype='float32')
            # y = choice(['duck','reset'])
            # y = choice([[0,1,0],[0,0,1]])
            y = [0, 1, 1]

            # x = [] # shape (1, 12)
        y = np.reshape(np.array(y), (1, 3))

        self.model = ann.train(self.model, x, y)

    def get_gene(self):
        # return updated gene when called
        # need to extract weights from the NN
        l1_weights = self.layer1.get_weights()  # 12*14 nodes
        ol_weights = self.out_layer.get_weights()  # 14*3 nodes
        gene = np.append(l1_weights[0], ol_weights[0])
        return np.array(gene)  # considering only weights here


# TODO: to here

class MarioGroup(Group):
    def __init__(self):
        super().__init__()

    def reset_pos(self):
        for sprite in self.sprites():
            sprite.reset_pos()
