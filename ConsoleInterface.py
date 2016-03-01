import sys
from Player import Player
from Game import Game
from GameEvent import GameEvent


class ConsoleInterface:

    def __init__(self):
        pass                    
        

    def handle_events(self):
        game_event = None
        action = ""
        while action != "W" and action != "M" and action != "P" and action != "Q":
            action = raw_input("Choose (W)all, (M)ove, (P)ass, (Q)uit: ")
        if action == "P":
            game_event = GameEvent("PASS")
        elif action == "Q":
            game_event = GameEvent("EXIT")
        elif action == "W" or action == "M":
            x = -1
            y = -1
            while x < 0 or x > 8 or y < 0 or y > 8:
                input = raw_input("Input the space coordinate (0,0 to 8,8): ")
                coords = input.split(",")
                if len(coords) != 2:
                    continue;
                try:
                    x = int(coords[0])
                    y = int(coords[1])
                except ValueError:
                    x = -1
                    y = -1
            game_event = GameEvent("SPACE")
            game_event.x = x
            game_event.y = y
            if action == "W":
                side = ""
                while side != "TOP" and side != "BOTTOM" and side != "LEFT" and side != "RIGHT":
                    side = raw_input("Please specify the side (TOP, BOTTOM, LEFT, RIGHT): ")
                game_event.section = side
                game_event.move_mode = "WALL"
            else:
                game_event.section = "CENTER"
                game_event.move_mode = "PAWN"

        return game_event 


    def draw_game(self, game):
        # draw game
        self.draw_board(game.board)
        pass
            

    def clear_space(self, x, y):
        pass

    
    def print_player_message(self, game):
        print game.player_message

    def print_game_message(self, game):
        print game.game_message
    

    def draw_board(self, board):
        print ""
        print "    0  1  2  3  4  5  6  7  8"
        print "_____________________________________________"        
        for y in range(9):
            row_output1 = " | "
            row_output2 = str(y) + "| "
            row_output3 = " | "
            for x in range(9):
                space = board.get(x, y)
                if space.top_has_wall:
                    row_output1 = row_output1 + "---"
                else:
                    row_output1 = row_output1 + "   "
                if space.left_has_wall:
                    row_output2 = row_output2 + "|"
                else:
                    row_output2 = row_output2 + " "
                if space.occupied_by_player != None:
                    row_output2 = row_output2 + str(space.occupied_by_player.number + 1)
                else:
                    row_output2 = row_output2 + "O"
                if space.right_has_wall:
                    row_output2 = row_output2 + "|"
                else:
                    row_output2 = row_output2 + " "

            print row_output1
            print row_output2
        print "_____________________________________________"        
        print ""


    def draw_board2(self, board):
        print ""
        print "    0    1    2    3    4    5    6    7    8"
        print "_____________________________________________"        
        for y in range(9):
            row_output1 = " | "
            row_output2 = str(y) + "| "
            row_output3 = " | "
            for x in range(9):
                space = board.get(x, y)
                if space.top_has_wall:
                    row_output1 = row_output1 + "___"
                else:
                    row_output1 = row_output1 + "   "
                if space.bottom_has_wall:
                    row_output3 = row_output3 + "---"
                else:
                    row_output3 = row_output3 + "   "
                if space.left_has_wall:
                    row_output2 = row_output2 + "|"
                else:
                    row_output2 = row_output2 + " "
                if space.occupied_by_player != None:
                    row_output2 = row_output2 + str(space.occupied_by_player.number + 1)
                else:
                    row_output2 = row_output2 + "O"
                if space.right_has_wall:
                    row_output2 = row_output2 + "|"
                else:
                    row_output2 = row_output2 + " "
                row_output1 = row_output1 + "  "
                row_output2 = row_output2 + "  "
                row_output3 = row_output3 + "  "

            print row_output1
            print row_output2
            print row_output3
        print "_____________________________________________"        
        print ""

