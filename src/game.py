from dataclasses import dataclass
from src.defaults import DEFAULT_SCREEN_HEIGHT, DEFAULT_SCREEN_WIDTH
import pygame

@dataclass
class Screen:

    screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT))
    screen_width = DEFAULT_SCREEN_WIDTH
    screen_height = DEFAULT_SCREEN_HEIGHT

class Game:
    def __init__(self, screen_width, screen_height):

        self.screen_handler = Screen(screen_width, screen_height)
        self.run_loop = True
        self.clock = pygame.time.Clock()
        self.objects_list: list= [] # Array for future objects to be spawned

    # Have to run this method first before carrying on with the simulation
    def init_game(self, objects_array: list = [], fps: int = 60):

        self.objects_list = objects_array
        self.run_loop = True
        self.fps = fps

    def run(self, epochs: int = 100):
     
            for epoch in range(epochs):
                    
                while self.run_loop:

                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT: 
                            self.run_loop = False # Exiting when wanting to exit

                    self.screen_handler.screen.fill((0, 0, 0))

                    if len(self.objects_list) != 0:
                        for object in self.objects_list:
                            object.draw(self.screen_handler.screen)

                    self.clock.tick(self.fps)
                    pygame.display.flip()

                if self.run_loop != True:
                    break
