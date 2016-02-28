import sys
from Space import Space
from GameEvent import GameEvent

class AI:

    def __init__(self, game):
        self._game = game.clone()
    
    # Check if the space that the player is in, is connected to the victory row.
    def is_connected(self, p):
        print "is_connected"
        connected = False
        player = self._game.players[p.number]
        graph = self.create_graph(self._game.board, player)
        connected_spaces = self.find_connected_spaces(self._game.board, graph, player.win_row)
        if player.position in connected_spaces:
            connected = True
        del connected_spaces[:]
        return connected
        
    def find_a_path(self, player):
        graph = self.create_graph(self._game.board, player)
        start = player.position
        end = self._game.board.get(0, player.win_row)
        path = []
        path = self.find_path(graph, start, end, path)        
        return path   



    def get_distance(self, player, board):
        graph = self.create_graph(board, player)   
        space_distances = self.calculate_space_distances(board, graph, player.win_row)
        distance = -1
        if space_distances.has_key(player.position):
            distance = space_distances[player.position]
        return distance
        

    def find_shortest_path(self, player, board):
        print "find_shortest_path for " + str(player)
        graph = self.create_graph(board, player)
        start = player.position
        # TODO:  is this a problem having x=0 here?
        #end = self._game.board.get(0, player.win_row)
        end = board.get(0, player.win_row)
        path = []
        shortest_path = self.find_shortest_path2(graph, start, end, path)
        return shortest_path
                
        
    def find_path(self, graph, start, end, path=[]):
        path = path + [start]
        if start.y == end.y:
            return path
        if not graph.has_key(start):
            return None
        if len(path) > 30:
            return None
        for node in graph[start]:
            if node not in path:
                newpath = self.find_path(graph, node, end, path)
                if newpath: return newpath
        return None


    def find_shortest_path2(self, graph, start, end, path=[], shortest_len=0, top_call=True):
        path = path + [start]
        if start.y == end.y:
            return path
        if not graph.has_key(start):
            return None
        shortest = None
        if (len(path) >= shortest_len-1 and shortest_len > 0) or len(path) > 30:
            return None
        for node in graph[start]:
            if node not in path and (len(path) < shortest_len-1 or shortest_len == 0):
                newpath = self.find_shortest_path2(graph, node, end, path, shortest_len, False)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
                        shortest_len = len(shortest)
                        if shortest_len <= abs(start.y - end.y):
                            return shortest
        return shortest        

    def create_graph(self, board, player):
        print "create_graph"
        graph = {}
        for x in range(9):
            for y in range(9): 
                space = board.get(x, y)  
                to_cells = []
                if y > 0 and space.top_has_wall == False:
                    top = board.get(x, y-1)
                    if top.bottom_has_wall == False: # and (top.occupied_by_player == None or top.occupied_by_player.number == player.number):
                        to_cells.append(top)  
                    #else:
                    #    if top.y > 0 and top.top_has_wall == False:
                    #        top = board.get(x, y-2)
                    #        to_cells.append(top)                    
                if y < 8 and space.bottom_has_wall == False:
                    bottom = board.get(x, y+1)
                    if bottom.top_has_wall == False: # and (bottom.occupied_by_player == None or bottom.occupied_by_player.number == player.number):
                        to_cells.append(bottom)                      
                    #else:
                    #    if bottom.y < 8 and bottom.bottom_has_wall == False:
                    #        bottom = board.get(x, y+2)
                    #        to_cells.append(bottom)                                                                    
                if x > 0 and space.left_has_wall == False:
                    left = board.get(x-1, y)
                    if left.right_has_wall == False: # and (left.occupied_by_player == None or left.occupied_by_player.number == player.number):
                        to_cells.append(left)      
                    #else:
                    #    if left.x > 0 and left.left_has_wall == False:
                    #        left = board.get(x-2, y)
                    #        to_cells.append(left)                            
                if x < 8 and space.right_has_wall == False:
                    right = board.get(x+1, y)
                    if right.left_has_wall == False: # and (right.occupied_by_player == None or right.occupied_by_player.number == player.number):
                        to_cells.append(right) 
                    #else:
                    #    if right.x < 8 and right.right_has_wall == False:
                    #        right = board.get(x+2, y)
                    #        to_cells.append(right)                           

                graph[space] = to_cells
        return graph

    def output_graph(self, graph, board):
        for x in range(9):
            for y in range(9):
                space = board.get(x, y)
                if graph.has_key(space):
                    print x, y, "->", graph[space]
                else:
                    print x, y, "->", None


    def calculate_space_distance(self, board, graph, victory_row, space_distances, x, y):
        space = board.get(x, y)
        if y == victory_row:
            space_distances[space] = 0

        # Try to get the distance for this space from its nodes
        elif graph.has_key(space): # and not space_distances.has_key(space):    
            for node in graph[space]:
                if graph.has_key(node) and space_distances.has_key(node):
                    distance = space_distances[node]
                    if not space_distances.has_key(space) or space_distances[space] > distance+1:
                        space_distances[space] = distance + 1

        # Populate the distances for its nodes
        if graph.has_key(space) and space_distances.has_key(space):
            distance = space_distances[space]
            for node in graph[space]:
                if not space_distances.has_key(node) or space_distances[node] > distance+1:
                    if node.y == victory_row:
                        space_distances[node] = 0
                    else:
                        space_distances[node] = distance + 1
                    # If a node distance was just determined, we want it to share the love to its siblings too
                    self.calculate_space_distance(board, graph, victory_row, space_distances, node.x, node.y)

    def calculate_space_distances(self, board, graph, victory_row):
        print "calculate_space_distances"
        space_distances = {}
        y = victory_row

        # We need to loop just in case the cols in the victory row have walls between them.
        for col in range(9):
            x = col
            self.calculate_space_distance(board, graph, victory_row, space_distances, x, y)
        self.calculate_space_distance(board, graph, victory_row, space_distances, 0, 0)
        self.calculate_space_distance(board, graph, victory_row, space_distances, 8, 8)

        # Return here to turn-off output of space_distances
        return space_distances
        for row in range(9):
            output = ""
            for col in range(9):                
                x = col
                y = row
                space = board.get(x,y)
                if space_distances.has_key(space):
                    output = output + " " + str(space_distances[space])
                else:
                    output = output + " ?"
            print output
        print " "
        return space_distances            
                        

    def find_connected_spaces(self, board, graph, victory_row):
        print "find_connected_spaces"
        space_distances = self.calculate_space_distances(board, graph, victory_row)
        connected_spaces = space_distances.keys()
        return connected_spaces            

    def determine_next_move(self, p):
        print "determine_next_move for " + str(p)
        game = self._game
        player = game.players[p.number]

        best_total = -99
        game_event = GameEvent("SPACE")

        for x in range(9):
            for y in range(9): 
                side = "TOP"
                placed = game.place_wall(player, x, y, side)
                if placed:
                    total = self.evaluate_game(game, player)
                    player.unplayed_wall_count = player.unplayed_wall_count + 1
                    game.unset_wall(x, y, side)
                    if total > best_total:
                        best_total = total
                        game_event.x = x
                        game_event.y = y
                        game_event.section = side
                        game_event.move_mode = "WALL"
                side = "BOTTOM"
                placed = game.place_wall(player, x, y, side)
                if placed:
                    total = self.evaluate_game(game, player)
                    player.unplayed_wall_count = player.unplayed_wall_count + 1
                    game.unset_wall(x, y, side)
                    if total > best_total:
                        best_total = total
                        game_event.x = x
                        game_event.y = y
                        game_event.section = side 
                        game_event.move_mode = "WALL"
                side = "LEFT"
                placed = game.place_wall(player, x, y, side)
                if placed:
                    total = self.evaluate_game(game, player)
                    player.unplayed_wall_count = player.unplayed_wall_count + 1
                    game.unset_wall(x, y, side)
                    if total > best_total:
                        best_total = total                        
                        game_event.x = x
                        game_event.y = y
                        game_event.section = side
                        game_event.move_mode = "WALL"
                side = "RIGHT"
                placed = game.place_wall(player, x, y, side)
                if placed:
                    total = self.evaluate_game(game, player)
                    player.unplayed_wall_count = player.unplayed_wall_count + 1
                    game.unset_wall(x, y, side)
                    if total > best_total:
                        best_total = total
                        game_event.x = x
                        game_event.y = y
                        game_event.section = side
                        game_event.move_mode = "WALL"

        print "best total from walls=" + str(best_total)
        path = self.find_shortest_path(player, game.board)
        print path
        if path != None and len(path) > 1:            
            next_space = path[1]
            moved = game.move_player(player, next_space.x, next_space.y)
            if moved:
                total = self.evaluate_game(game, player, True)
            else:
                print "determine_next_move: not moving", next_space.x, next_space.y
                total = -99
            print "move_total=" + str(total)
            if total > best_total:
                best_total = total
                game_event = GameEvent("SPACE")
                space = path[1]
                game_event.x = space.x
                game_event.y = space.y
                game_event.section = "CENTER"
                game_event.move_mode = "PAWN"
        return game_event

    def evaluate_game(self, game, player, moved=False):
        p1 = game.players[0]   
        p2 = game.players[1]
        if p1.name == player.name:
            p1.unplayed_wall_count = player.unplayed_wall_count
        else:
            p2.unplayed_wall_count = player.unplayed_wall_count
        sp1 = self.get_distance(p1, game.board)
        sp2 = self.get_distance(p2, game.board)
        wc1 = p1.unplayed_wall_count
        wc2 = p2.unplayed_wall_count
        cp = game.current_player
        total = 0

        if moved == False:
            total = total + 1        
        if cp == 0:
            total = (sp2 - sp1)*2 + (wc1-wc2)
        else:
            total = (sp1 - sp2)*2 + (wc2-wc1)
        #print "dist1=%s, dist2=%s, wall1=%s, wall2=%s, current=%s => %s" \
        #    % (sp1, sp2, wc1, wc2, cp, total)  
        return total
                        
    
    def print_path(self, path):
        for space in path:
            sys.stdout.write(str(space))
        print ""
            
    def print_board(self, game):
        for x in range(9):
            for y in range(9):                    
                space = game.board.get(x,y)
                print str(x) + "," + str(y) + " " + str(space.occupied_by_player)
            
                