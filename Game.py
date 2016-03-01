import sys
from Board import Board
from AI import AI
from GameEvent import GameEvent
from Logger import log


class Game:
    
    def __init__(self):
        self.players = []
        self.board = None
        self.current_player = 0
        self.turn = 0
        self.game_message = ""
        self.player_message = ""
        self.old_game_message = ""
        self.old_player_message = ""
        self.interface = None

      
    def init_two_player_game(self, p1, p2):
        log("init_two_player_game", 1, 2)
        p1.unplayed_wall_count = 10
        p2.unplayed_wall_count = 10
        self.board = Board()
        self.board.initialize()
        self.players.append(p1)
        p1.number = 0
        self.players.append(p2)
        p2.number = 1
        self.move_player(p1, 4, 0)
        p1.win_row = 8
        self.move_player(p2, 4, 8)
        p2.win_row = 0
        self.current_player = 0

    # Puts a player at the specified location on the game board.
    def place_player(self, player, x, y):
        # clear the old position
        if player.position != None:
            player.position.occupied_by_player = None
            player.position = None
          
        self.board.get(x,y).occupied_by_player = player
        player.position = self.board.get(x,y)
        moved = True
        return moved      
        
    # Tries to move the player to the specified location.
    def move_player(self, player, x, y):
        moved = False
        is_valid = self.validate_move(player, x, y)
        if is_valid:
            self.place_player(player, x, y)
            
            moved = True
        return moved

    # Checks whether it is valid to place a wall at the specified location.
    def validate_wall(self, x, y, side):
        log("validate_wall", x, y, side)
        is_ok = True
        placed = self.set_wall(x, y, side)
        #ai = AI(self)
        if placed:
            for p in self.players:
                log(p.name, p.win_row)
                if is_ok:
                    if not self.board.is_connected(p.position, p.win_row):
                        log("not connected")
                        is_ok = False
        else:
            is_ok = False
        if placed:
            self.unset_wall(x, y, side)
        return is_ok
        
    # Places a wall at the specified location.
    def set_wall(self, x, y, side):
        log("set_wall():", x,y, side)
        placed = False
        if side == "TOP":
            if y <= 0:
                log("TOP y<=0")
                return placed
            if x >= 8:
                log("TOP x>=8")
                return placed
            if self.board.get(x,y).top_has_wall:
                log("TOP (x,y).top_has_wall")
                return placed
            if self.board.get(x+1,y).top_has_wall:
                log("TOP (x+1,y).top_has_wall")
                return placed
            if self.board.get(x,y-1).right_has_wall and self.board.get(x,y).right_has_wall:
                log("TOP (x,y-1).right_has_wall and (x,y).right_has_wall")
                return placed
            placed = True
            self.board.get(x,y).top_has_wall = True
            self.board.get(x+1,y).top_has_wall = True
            if y > 0:
                self.board.get(x,y-1).bottom_has_wall = True
                self.board.get(x+1,y-1).bottom_has_wall = True

        elif side == "BOTTOM":
            if y >= 8:
                log("BOTTOM y >= 8")
                return placed
            if x >= 8:
                log("BOTTOM x >= 8")
                return placed
            if self.board.get(x,y).bottom_has_wall:
                log("BOTTOM (x,y).bottom_has_wall")
                return placed
            if self.board.get(x+1,y).bottom_has_wall:
                log("BOTTOM (x+1,y).bottom_has_wall")
                return placed
            if self.board.get(x,y+1).right_has_wall and self.board.get(x,y).right_has_wall:
                log("BOTTOM (x,y+1).right_has_wall and (x,y).right_has_wall")
                return placed
            placed = True
            self.board.get(x,y).bottom_has_wall = True
            self.board.get(x+1,y).bottom_has_wall = True            
            if y < 8:
                self.board.get(x,y+1).top_has_wall = True
                self.board.get(x+1,y+1).top_has_wall = True

        elif side == "LEFT":
            if x <= 0:
                log("LEFT x <= 0")
                return placed
            if y >= 8:
                log("LEFT y >= 8")
                return placed
            if self.board.get(x,y).left_has_wall:
                log("LEFT (x,y).left_has_wall")
                return placed
            if  self.board.get(x,y+1).left_has_wall:
                log("LEFT (x,y+1).left_has_wall")
                return placed
            if self.board.get(x-1,y).bottom_has_wall and self.board.get(x,y).bottom_has_wall:
                log("LEFT (x-1,y).bottom_has_wall and (x,y).bottom_has_wall")
                return placed
            placed = True
            self.board.get(x,y).left_has_wall = True
            self.board.get(x,y+1).left_has_wall = True
            if x < 8:
                self.board.get(x-1,y).right_has_wall = True
                self.board.get(x-1,y+1).right_has_wall = True

        elif side == "RIGHT":
            if x >= 8:
                log("RIGHT x >= 8")
                return placed
            if y >= 8:
                log("RIGHT y >= 8")
                return placed
            if self.board.get(x,y).right_has_wall:
                log("RIGHT (x,y).right_has_wall")
                return placed
            if self.board.get(x,y+1).right_has_wall:
                log("RIGHT (x,y+1).right_has_wall")
                return placed
            if self.board.get(x,y).bottom_has_wall and self.board.get(x+1,y).bottom_has_wall:
                log("RIGHT (x,y).bottom_has_wall and (x+1,y).bottom_has_wall")
                return placed
            placed = True
            self.board.get(x,y).right_has_wall = True
            self.board.get(x,y+1).right_has_wall = True
            if x > 0:
                self.board.get(x+1,y).left_has_wall = True
                self.board.get(x+1,y+1).left_has_wall = True
        return placed

    def unset_wall(self, x, y, side):
        if side == "TOP" and y > 0:
            self.board.get(x,y).top_has_wall = False
            self.board.get(x+1,y).top_has_wall = False
            if y < 9:
                self.board.get(x,y-1).bottom_has_wall = False
                self.board.get(x+1,y-1).bottom_has_wall = False
        elif side == "BOTTOM" and y < 8:
            self.board.get(x,y).bottom_has_wall = False
            self.board.get(x+1,y).bottom_has_wall = False
            if y >= 0:
                self.board.get(x,y+1).top_has_wall = False
                self.board.get(x+1,y+1).top_has_wall = False
        elif side == "LEFT" and x > 0:
            self.board.get(x,y).left_has_wall = False
            self.board.get(x,y+1).left_has_wall = False
            if x < 9:
                self.board.get(x-1,y).right_has_wall = False
                self.board.get(x-1,y+1).right_has_wall = False
        elif side == "RIGHT" and x < 8:
            self.board.get(x,y).right_has_wall = False
            self.board.get(x,y+1).right_has_wall = False
            if x >= 0:
                self.board.get(x+1,y).left_has_wall = False
                self.board.get(x+1,y+1).left_has_wall = False


    # Tries to place a wall at the specified location  
    def place_wall(self, player, x, y, side):
        log("place_wall", x, y, side)
        placed = False
        is_ok = self.validate_wall(x, y, side)
        if is_ok and x >= 0 and x <= 8 and y >= 0 and y <= 8:
            if player.unplayed_wall_count > 0:
                placed = self.set_wall(x, y, side)
                if placed:
                    player.unplayed_wall_count = player.unplayed_wall_count - 1
        return placed

    def end_turn(self):
        player = self.players[self.current_player]
        player.move_mode = None
        self.current_player = self.current_player + 1
        if self.current_player >= len(self.players):
            self.current_player = 0
        self.begin_turn()
        

    def begin_turn(self):
        self.turn = self.turn + 1
        log("turn=", self.turn)
        player = self.players[self.current_player]
        self.output_player_message(player.name + ", your turn. walls=" + str(self.players[0].unplayed_wall_count) + ", " + str(self.players[1].unplayed_wall_count))

    # Checks whether the player can be placed at the specified location.
    def validate_move(self, player, x, y):
        log("validate_move")
        space = None
        is_ok = True
        if player.position != None:
            old_x = player.position.x
            old_y = player.position.y
            if x < 0 or x > 8 or y < 0 or y > 8:
                log("validate_move: move out of bounds", x, y)
                is_ok = False
            if is_ok:
                ai = AI(self)
                graph = self.board.create_graph()
                if graph.has_key(player.position):
                    nodes = graph[player.position]
                    space = self.board.get(x, y) 
                    if not space in nodes:
                        log("validate_move: space not in connected node", x, y)
                        is_ok = False
                else:
                    log("validate_move: space not in graph", x, y)
                    is_ok = False        
            if is_ok:
                space = self.board.get(x, y)  
                if space.occupied_by_player:
                    log("validate_move: space occupied by another player", x, y)
                    is_ok = False                                                          
        return is_ok       

    # Checks if the player has reached the victory row
    def check_victory(self, player):
        victory = False
        if player == None:
            player = self.players[self.current_player]
        if player.win_col != None and player.win_col == player.position.x:
            victory = True
        if player.win_row != None and player.win_row == player.position.y:
            victory = True            
        return victory
        
    # Main game loop logic
    def game_loop(self, interface):
        self.interface = interface
        game_over = False
        self.begin_turn()
        interface.draw_game(self) 
        victory = False       
        while not game_over:
            player = self.players[self.current_player]
            game_event = None

            if player.is_computer and not victory:
                log("game_loop: for " + str(player))
                ai = AI(self)
                game_event = ai.determine_next_move(player)
                log("game_loop: game_event=", game_event)
                player.move_mode = game_event.move_mode
                #exit(0);
            else:
                game_event = interface.handle_events()
                player.move_mode = game_event.move_mode

            if game_event == None:
                pass 
            elif game_event.name == "PASS":
                self.end_turn();
                continue;
            elif game_event.name == "EXIT":
                game_over = True
            elif game_event.name == "SPACE" and not victory:

                space = self.board.get(game_event.x,game_event.y)
                if game_event.section == "CENTER" and \
                   space.occupied_by_player == player:
                    player.move_mode = "PAWN" 
                    self.output_player_message(player.name + ", move your pawn")
                             
                elif game_event.section != "CENTER" and player.move_mode != "WALL" and player.unplayed_wall_count > 0:
                    player.move_mode = "WALL"
                    self.output_player_message(player.name + ", place a wall - " + str(player.unplayed_wall_count) + " left")

                else:
                    if player.move_mode == "PAWN":
                        old_position = player.position
                        moved = self.move_player(player, game_event.x, game_event.y)
                        if moved:
                            interface.clear_space(old_position.x, old_position.y)
                            if self.check_victory(None):
                                #game_over = True
                                victory = True
                                self.output_player_message(player.name + ", you won!")
                            else:
                                self.end_turn()
                            interface.draw_game(self)
                        
                    elif player.move_mode == "WALL":
                        placed = self.place_wall(player, 
                                                 game_event.x, game_event.y, 
                                                 game_event.section)    
                        if placed:         
                            self.end_turn()
                            interface.draw_game(self)

    def output_player_message(self, msg):
        self.old_player_message = self.player_message
        self.player_message = msg
        self.interface.print_player_message(self)
                
    def clone(self):
        g = Game()
        new_board = self.board.clone()   
        g.board = new_board
        g.current_player = self.current_player
        g.turn = self.turn        
        g.players = []
        for p in self.players:
            player = p.clone()
            player_x = p.position.x
            player_y = p.position.y
            g.place_player(player, player_x, player_y)
            g.players.append(player)
        return g

    # To string method
    def __str__(self):
        output = ""
        output = output + "turn=" + str(self.turn)
        output = output + "\n"
        output = output + "current_player=" + str(self.current_player)
        output = output + "\n"
        output = output + "players=" + str(self.players)
        output = output + "\n"
        output = output + str(self.board) 
        return output
                

                