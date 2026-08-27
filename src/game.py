from dataclasses import dataclass
from src.defaults import DEFAULT_SCREEN_HEIGHT, DEFAULT_SCREEN_WIDTH, DEFAULT_TIME_LIMIT
from src.game_objects import StrappedObject, Target
import pygame

@dataclass
class Screen:

    screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT))
    screen_width = DEFAULT_SCREEN_WIDTH
    screen_height = DEFAULT_SCREEN_HEIGHT

class Game:
    def __init__(self, screen_width, screen_height):

        self.screen_handler = Screen()
        self.run_loop = True
        self.clock = pygame.time.Clock()
        self.objects_list: list = [] # Array for future objects to be spawned
        self.targets_list: list[Target] = [] # Array for storing targets

    # Have to run this method first before carrying on with the simulation
    def init_game(self, targets_list: list = [], objects_array: list = [], fps: int = 60):

        self.objects_list = objects_array
        self.targets_list = targets_list
        self.run_loop = True
        self.fps = fps

    def run(self, epochs: int = 100):

            self.count = 0

            for epoch in range(epochs):
                    
                while self.run_loop:

                    if self.count == DEFAULT_TIME_LIMIT:
                        self.run_loop = False

                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT: 
                            self.run_loop = False # Exiting when wanting to exit

                    self.screen_handler.screen.fill((0, 0, 0))

                    print(self.targets_list)

                    if len(self.targets_list) != 0:
                        for target in self.targets_list:
                            if type(target) == int:
                                continue

                            else:
                                target.draw(self.screen_handler.screen)
                            
                    if len(self.objects_list) != 0:
                        for obj in self.objects_list:

                            if type(obj) != StrappedObject:
                                obj.run(self.screen_handler.screen)
                            else:
                                obj.run(self.targets_list, self.screen_handler.screen)
                            

                    self.clock.tick(self.fps)
                    pygame.display.flip()

                    self.count += 1

                if not self.run_loop and self.count <= DEFAULT_TIME_LIMIT:
                    break

               
                self.run_loop = True
                self.count = 0

                # Apply inheritance, mutation and new spawn logic here
                #   1. Check Best(best 2 candidates)
                #   2. Mix the weights of the two candidates randomly
                #   3. Spawn more instances with the mixed wieghts
                #   4. Apply Mutation on a percentage of the population
                #   5. Run simulation again