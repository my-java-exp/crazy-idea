# Strap networks on them
import pygame
import numpy
import random
from keyboard import is_pressed

from src.defaults import DEFAULT_OBJECTS_COLOUR, DEFAULT_HIDDEN_COUNT, DEFAULT_TARGET_CONFIG, DEFAULT_AI_MOVEMENT
from src.networks import Base
from src.functions import collision_check

def distance(x1, x2, y1, y2):
    return numpy.sqrt((x1 - x2)**2 + (y1 - y2)**2)

class Target(pygame.Rect):
    def __init__(self, max_x, max_y):

        self.width = DEFAULT_TARGET_CONFIG["width"]
        self.height = DEFAULT_TARGET_CONFIG["height"]

        self.x = random.randrange(min, max_x)
        self.y = random.randrange(min, max_y)

class BaseObject:
    def __init__(self, height: int, width: int, min_int: int, max_x: int, max_y: int): # Min Max are just variables for the coordinates, going for the min=0 to the max=SCREEN_WIDTH/HEIGHT
        self.x = random.randrange(min_int, max_x)
        self.y = random.randrange(min_int, max_y)
        self.max_x = max_x
        self.max_y = max_y
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def draw(self, screen: pygame.Surface, colour: tuple[int, int, int] = DEFAULT_OBJECTS_COLOUR):
        pygame.draw.rect(screen, colour, self.rect)

    def check_wall_collision(self):

        if self.x < 0:
            self.x = self.max_x - self.rect.width
            self.rect.x = self.x

        elif self.x + self.rect.width > self.max_x:
            self.x = 0
            self.rect.x = self.x

        if self.y < 0:
            self.y = self.max_y - self.rect.height
            self.rect.y = self.y

        elif self.y + self.rect.height > self.max_y:
            self.y = 0
            self.rect.y = self.y

        return 1

    def run(self, screen: pygame.Surface):
        self.draw(screen=screen)


class UserObject(BaseObject):
    def __init__(self, height: int, width: int, min_int: int, max_x: int, max_y: int):
        super().__init__(height, width, min_int, max_x, max_y)

        self.x = random.randrange(min_int, max_x)
        self.y = random.randrange(min_int, max_y)
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def movement(self):

        if is_pressed("w"):
            self.y += -1

        elif is_pressed("s"):
            self.y += 1

        if is_pressed("a"):
            self.x += -1

        elif is_pressed("d"):
            self.x += 1

        self.rect.y = self.y
        self.rect.x = self.x

    def check_obj_collision(self, collide_list):

        collide_list = self.rect.collidelist(collide_list)

    def run(self, screen: pygame.Surface):
        self.movement()
        self.check_wall_collision()
        self.draw(screen=screen, colour=(83, 21, 44))

class StrappedObject(BaseObject):
    def __init__(self, height: int, width: int, min_int: int, max_x: int, max_y: int, input_dim: int, hidden_dim: int, output_dim, hidden_count: int=DEFAULT_HIDDEN_COUNT):
        super().__init__(height, width, min_int, max_x, max_y)
        self.network = Base(input_dim, hidden_dim, output_dim, hidden_count=hidden_count)
        self.x = random.randrange(min_int, max_x)
        self.y = random.randrange(min_int, max_y)

        self.rect.x = self.x
        self.rect.y = self.y

        self.previous_reward = 0
        self.current_reward = 0

    def movement(self, targets):

        self.previous_reward = self.current_reward

        new_targets = [target for target in targets if distance(target.x, self.x, target.y, self.y)]
        state = numpy.array([self._calc_data()])
        logits = self.network(state)

        predicted_move = numpy.argmax(logits)

        self.x += DEFAULT_AI_MOVEMENT.get(predicted_move, 0)[0]
        self.y += DEFAULT_AI_MOVEMENT.get(predicted_move, 0)[1]

        if len(new_targets) != 0:
            for target in new_targets:
        
                val = collision_check(target, self.rect)
                if val == 0:
                    self.current_reward += 0.5

                else:
                    self.current_reward = val

        else:
            self.current_reward = 0

        self.rect.x = self.x
        self.rect.y = self.y
    def run(self, targets_array, screen: pygame.Surface):

        self.movement(targets_array)
        self.check_wall_collision()
        self.draw(screen=screen)
        
        
    def _calc_data(self):
        return [self.x, self.y, self.previous_reward]