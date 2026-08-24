import numpy
import src.networks
import src.game as game
import src.game_objects as obj

test_input = numpy.random.rand(4, 2)

Game = game.Game(500, 500)
Game.init_game([obj.StrappedObject(10, 10, 0, Game.screen_handler.screen_width, Game.screen_handler.screen_height, 3, 5, 4)])
Game.run(20)