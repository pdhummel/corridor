import sys, pygame
from pygame.locals import *
from Player import Player
from Game import Game
from GameEvent import GameEvent
from PyGameInterface import PyGameInterface
from PyGameInterface import black, red, white, gray, blue
from ConsoleInterface import ConsoleInterface

interface = PyGameInterface()
#interface = ConsoleInterface()

                        
# setup data
p1 = Player()
p1.name = "Paul (red)"
#p1.name = "AI (red)"
p1.color = red
p1.is_computer = True
p2 = Player()
p2.name = "AI (blue)"
#p2.name = "Paul (blue)"
p2.is_computer = True
p2.color = blue
game = Game()
game.init_two_player_game(p1, p2)
game.game_loop(interface)






