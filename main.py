import numpy
import src.networks
import src.game as game
import src.game_objects as obj
from src.defaults import DEFAULT_AI_POPULATION, DEFAULT_TARGET_COUNT

# DO NOT RUN ANYTHING BECAUSE THIS PROJECT IS INCOMPLETE

Game = game.Game(500, 500)
objects_list = [obj.StrappedObject(10, 10, 0, Game.screen_handler.screen_width, Game.screen_handler.screen_height, 3, 5, 4, 3) for _ in range(DEFAULT_AI_POPULATION)]
targets_list = [obj.Target(0, Game.screen_handler.screen_width, Game.screen_handler.screen_height) for _ in range(DEFAULT_TARGET_COUNT)]
Game.init_game(targets_list, objects_list)
Game.run(20)