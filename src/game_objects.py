# Strap networks on them
import pygame
import numpy
from src.defaults import DEFAULT_OBJECTS_COLOUR, DEFAULT_HIDDEN_COUNT, DEFAULT_TARGET_CONFIG
from src.networks import Base
from src.functions import collision_check

def distance(x1, x2, y1, y2):
    return numpy.sqrt((x1 - x2)**2 + (y1 - y2)**2)

class Target(pygame.Rect):
    def __init__(self, max_x, max_y):

        self.width = DEFAULT_TARGET_CONFIG["width"]
        self.height = DEFAULT_TARGET_CONFIG["height"]

        self.x = numpy.random.randint(min, max_x)
        self.y = numpy.random.randint(min, max_y)

class BaseObject:
    def __init__(self, height: int, width: int, min: int, max_x: int, max_y: int): # Min Max are just variables for the coordinates, going for the min=0 to the max=SCREEN_WIDTH/HEIGHT
        self.x = numpy.random.randint(min, max_x)
        self.y = numpy.random.randint(min, max_y)
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (DEFAULT_OBJECTS_COLOUR), self.rect)

class StrappedObject(BaseObject):
    def __init__(self, height: int, width: int, min: int, max_x: int, max_y: int, input_dim: int, hidden_dim: int, output_dim, hidden_count: int=DEFAULT_HIDDEN_COUNT):
        super().__init__(height, width, min, max_x, max_y)
        self.network = Base(input_dim, hidden_dim, output_dim, hidden_count=hidden_count)
        self.previous_reward = 0
        self.current_reward = 0

    def movement(self, targets):

        new_targets = [target for target in targets if distance(target.x, self.x, target.y, self.y)]
        state = numpy.array([self._calc_data(new_targets)])
        logits = self.network(state)

    def _calc_data(self, targets):

        # if its 10 blocks close to any block, give a small +1 reward else 0
        self.previous_reward = self.current_reward

        for target in targets:

            val = collision_check(target, self.rect)
            if val == 0:
                self.current_reward += 0.5

            else:
                self.current_reward = val

        
        return [self.x, self.y, self.previous_reward, self.current_reward]