import sys, pygame
from pygame.locals import *
from Player import Player
from Game import Game
from GameEvent import GameEvent
import pygame.font
import pygame.surface


black = 0, 0, 0
white = 255, 255, 255
gray = 190, 190, 190
red =  255, 0, 0
blue = 0, 0, 255

class PyGameInterface:

    def __init__(self):
        pygame.init()
        
        self.board_width = 1024
        self.board_height = 768
        self.space_width = 70
        self.space_height = 70
        self.left_margin = 150
        self.top_margin = 100
        self.pawn_size = 20    

        board_size = self.board_width, self.board_height
        self.screen = pygame.display.set_mode(board_size)
        self.screen.fill(black)
                    
        
    def get_board_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        
        x = (mouse_x-self.left_margin)/self.space_width 
        y = (mouse_y-self.top_margin)/self.space_height
        section = "CENTER"
        
        if mouse_x > self.space_width*x + self.left_margin and \
           mouse_x < self.space_width*x + self.left_margin + 7:
            section = "LEFT"
        elif mouse_x > self.space_width*x + self.left_margin + self.space_width - 7 and \
           mouse_x < self.space_width*x + self.left_margin + self.space_width:
            section = "RIGHT"            
        elif mouse_y > self.space_height*y + self.top_margin and \
           mouse_y < self.space_height*y + self.top_margin + 7:
            section = "TOP"        
        elif mouse_y > self.space_height*y + self.top_margin + self.space_height - 7 and \
           mouse_y < self.space_height*y + self.top_margin + self.space_height:
            section = "BOTTOM"              
        return x, y, section

                
    def get_mouse_game_event(self):
        space_x, space_y, section = self.get_board_pos()
        game_event = None
        if space_x < 0 or space_x > 8 or space_y < 0 or space_y > 8:
            game_event = GameEvent("NOOP")
        else:
            game_event = GameEvent("SPACE")
            game_event.x = space_x
            game_event.y = space_y
            game_event.section = section
        return game_event


    def handle_events(self):
        game_event = None
        for event in pygame.event.get():
            if event.type == QUIT:
                game_event = GameEvent("EXIT")
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                game_event = GameEvent("EXIT")
            elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                game_event = self.get_mouse_game_event()
            elif event.type == MOUSEBUTTONUP and pygame.mouse.get_pressed()[0]:
                game_event = self.get_mouse_game_event()
        if game_event == None:
            game_event = GameEvent("NOOP")
        return game_event 
            

    def draw_game(self, game):
        # draw game
        for x in range(9):
            for y in range(9):
                pygame.draw.rect(self.screen, gray, 
                                                (self.space_width*x + self.left_margin, 
                                                self.space_height*y + self.top_margin, 
                                                self.space_width, self.space_height), 1)
        for x in range(9):
            for y in range(9):
            	space = game.board.get(x,y)        
                if space.top_has_wall:
                    pygame.draw.line(self.screen, white, 
                                     (self.space_width*x + self.left_margin, self.space_height*y + self.top_margin), 
                                     (self.space_width*x + self.left_margin + self.space_width, self.space_height*y + self.top_margin), 
                                     10)
                if space.bottom_has_wall:
                    pygame.draw.line(self.screen, white, 
                                     (self.space_width*x + self.left_margin, self.space_height*(y+1) + self.top_margin), 
                                     (self.space_width*x + self.left_margin + self.space_width, self.space_height*(y+1) + self.top_margin), 
                                     10)
                if space.left_has_wall:
                    pygame.draw.line(self.screen, white, 
                                     (self.space_width*x + self.left_margin, self.space_height*y + self.top_margin), 
                                     (self.space_width*x + self.left_margin, self.space_height*y + self.top_margin + self.space_height), 
                                     10)
                if space.right_has_wall:
                    pygame.draw.line(self.screen, white, 
                                     (self.space_width*(x+1) + self.left_margin, self.space_height*y + self.top_margin), 
                                     (self.space_width*(x+1) + self.left_margin, self.space_height*y + self.top_margin + self.space_height), 
                                     10)
                if space.occupied_by_player != None:
                    player = space.occupied_by_player
                    pygame.draw.circle(self.screen, player.color, 
        			                   (self.space_width*x + self.left_margin + (self.space_width/2), 
        			                    self.space_height*y + self.top_margin + (self.space_height/2)),
        			                   self.pawn_size, 0)
        

        pygame.display.flip()

            

    def clear_space(self, x, y):
        pygame.draw.circle(self.screen, black, 
		                   (self.space_width*x + self.left_margin + (self.space_width/2), 
		                    self.space_height*y + self.top_margin + (self.space_height/2)),
		                   self.pawn_size, 0)


    
    def print_player_message(self, game):
        pygame.draw.rect(self.screen, black, (10, 30, 400, 20), 0)
        #self.game_print(game.old_player_message, 10, 30, black)
        if game.player_message != None:
            self.game_print(game.player_message, 10, 30, white)
        pygame.display.flip()        

    
    def print_game_message(self, game):
        pygame.draw.rect(self.screen, black, (10, 10, 400, 20), 0)
        #self.game_print(game.old_game_message, 10, 10, black)
        if game.player_message != None:
            self.game_print(game.game_message, 10, 10, white)   
        pygame.display.flip()      

    
    def game_print(self, text,xx,yy,color):
       font = pygame.font.SysFont("Courier New",18)
       ren = font.render(text,1,color)
       self.screen.blit(ren, (xx,yy))

