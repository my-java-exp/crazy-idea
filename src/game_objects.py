# Strap networks on them
import pygame
import numpy
from src.defaults import DEFAULT_OBJECTS_COLOUR, DEFAULT_HIDDEN_COUNT, DEFAULT_TARGET_CONFIG, DEFAULT_AI_MOVEMENT
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
        self.max_x = max_x
        self.max_y = max_y
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (DEFAULT_OBJECTS_COLOUR), self.rect)

    def check_wall_collision(self):

        if self.x < 0:
            self.x = self.max_x - self.rect.width
            self.rect.x = self.x

        elif self.x + self.rect.width > self.max_x:
            self.x = 0
            self.rect.x = self.x

        if self.x < 0:
            self.y = self.max_x - self.rect.height
            self.rect.y = self.y

        elif self.y + self.rect.height > self.max_y:
            self.y = 0
            self.rect.y = self.y
        
    def run(self, screen: pygame.Surface):
        self.draw(screen=screen)

class StrappedObject(BaseObject):
    def __init__(self, height: int, width: int, min: int, max_x: int, max_y: int, input_dim: int, hidden_dim: int, output_dim, hidden_count: int=DEFAULT_HIDDEN_COUNT):
        super().__init__(height, width, min, max_x, max_y)
        self.network = Base(input_dim, hidden_dim, output_dim, hidden_count=hidden_count)
        self.previous_reward = 0
        self.current_reward = 0

    def movement(self, targets):

        self.previous_reward = self.current_reward

        new_targets = [target for target in targets if distance(target.x, self.x, target.y, self.y)]
        state = numpy.array([self._calc_data()])
        print(type(state))
        print(state)
        logits = self.network(state)

        predicted_move = numpy.argmax(logits)

        self.x, self.y = DEFAULT_AI_MOVEMENT[predicted_move]
        self.rect.x, self.rect.y = self.x, self.y

        if len(targets) != 0:
            for target in targets:
        
                val = collision_check(target, self.rect)
                if val == 0:
                    self.current_reward += 0.5

                else:
                    self.current_reward = val

        else:
            self.current_reward = 0

        self.check_wall_collision()

    def run(self, targets_array, screen: pygame.Surface):

        self.movement(targets_array)
        self.draw(screen=screen)
        
    def _calc_data(self):
        return [self.x, self.y, self.previous_reward]