import sys
from Space import Space

class AI:

    def __init__(self, game):
        self._game = game
    
    def is_connected(self, player):
        connected = False
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
        graph = self.create_graph(board, player)
        start = player.position
        end = self._game.board.get(0, player.win_row)
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
                        #if top_call:
                        #     self.print_path(shortest)
                        shortest_len = len(shortest)
                        if shortest_len <= abs(start.y - end.y):
                            return shortest
        return shortest        

    def create_graph(self, board, player):
        graph = {}
        for x in range(9):
            for y in range(9): 
                space = board.get(x, y)  
                to_cells = []
                if y > 0 and space.top_has_wall == False:
                    top = board.get(x, y-1)
                    if top.bottom_has_wall == False and (top.occupied_by_player == None or top.occupied_by_player.number == player.number):
                        to_cells.append(top)  
                    else:
                        if top.y > 0 and top.top_has_wall == False:
                            top = board.get(x, y-2)
                            to_cells.append(top)                    
                if y < 8 and space.bottom_has_wall == False:
                    bottom = board.get(x, y+1)
                    if bottom.top_has_wall == False and (bottom.occupied_by_player == None or bottom.occupied_by_player.number == player.number):
                        to_cells.append(bottom)                      
                    else:
                        if bottom.y < 8 and bottom.bottom_has_wall == False:
                            bottom = board.get(x, y+2)
                            to_cells.append(bottom)                                                                    
                if x > 0 and space.left_has_wall == False:
                    left = board.get(x-1, y)
                    if left.right_has_wall == False and (left.occupied_by_player == None or left.occupied_by_player.number == player.number):
                        to_cells.append(left)      
                    else:
                        if left.x > 0 and left.left_has_wall == False:
                            left = board.get(x-2, y)
                            to_cells.append(left)                            
                if x < 8 and space.right_has_wall == False:
                    right = board.get(x+1, y)
                    if right.left_has_wall == False and (right.occupied_by_player == None or right.occupied_by_player.number == player.number):
                        to_cells.append(right) 
                    else:
                        if right.x < 8 and right.right_has_wall == False:
                            right = board.get(x+2, y)
                            to_cells.append(right)                           

                graph[space] = to_cells
            
        return graph




    def calculate_space_distances(self, board, graph, victory_row):
        space_distances = {}
        for row in range(9):
            y = row
            if victory_row == 8:
                y = 8 - row
            for col in range(9):
                x = col
                space = board.get(x, y)
                
                if y == victory_row:
                    space_distances[space] = 0
                
                if graph.has_key(space) and space_distances.has_key(space):
                    distance = space_distances[space]
                    for node in graph[space]:
                        if not space_distances.has_key(node) or space_distances[node] > distance+1:
                            space_distances[node] = distance + 1    
        for row in range(9):
            y = 8 - row
            if victory_row == 8:
                y = row
            for col in range(9):
                x = 8-col
                space = board.get(x, y)
                
                if y == victory_row:
                    space_distances[space] = 0
                
                if graph.has_key(space) and space_distances.has_key(space):
                    distance = space_distances[space]
                    for node in graph[space]:
                        if not space_distances.has_key(node) or space_distances[node] > distance+1:
                            space_distances[node] = distance + 1    
        for col in range(9):                    
            x = col
            for row in range(9):
                y = row
                if victory_row == 8:
                    y = 8 - row
            
                space = board.get(x, y)
                
                if y == victory_row:
                    space_distances[space] = 0
                
                if graph.has_key(space) and space_distances.has_key(space):
                    distance = space_distances[space]
                    for node in graph[space]:
                        if not space_distances.has_key(node) or space_distances[node] > distance+1:
                            space_distances[node] = distance + 1    
        for col in range(9):                    
            x = 8-col
            for row in range(9):
                y = row
                if victory_row == 8:
                    y = row
            
                space = board.get(x, y)
                
                if y == victory_row:
                    space_distances[space] = 0
                
                if graph.has_key(space) and space_distances.has_key(space):
                    distance = space_distances[space]
                    for node in graph[space]:
                        if not space_distances.has_key(node) or space_distances[node] > distance+1:
                            space_distances[node] = distance + 1    

        return space_distances            
                        

    def find_connected_spaces(self, board, graph, victory_row):
        space_distances = self.calculate_space_distances(board, graph, victory_row)
        connected_spaces = space_distances.keys()
        return connected_spaces            

    def determine_next_move(self, g, player):
        game = g.clone()
        for x in range(9):
            for y in range(9): 
                print str(x) + "," + str(y)
                side = "TOP"
                placed = game.place_wall(player, x, y, side)
                if placed:
                    self.evaluate_game(game, player)
                    player.unplayed_wall_count = player.unplayed_wall_count + 1
                    game.unset_wall(x, y, side)
                side = "BOTTOM"
                placed = game.place_wall(player, x, y, side)
                if placed:
                    self.evaluate_game(game, player)
                    player.unplayed_wall_count = player.unplayed_wall_count + 1
                    game.unset_wall(x, y, side)                
                side = "LEFT"
                placed = game.place_wall(player, x, y, side)
                if placed:
                    self.evaluate_game(game, player)
                    player.unplayed_wall_count = player.unplayed_wall_count + 1
                    game.unset_wall(x, y, side)                
                side = "RIGHT"
                placed = game.place_wall(player, x, y, side)
                if placed:
                    self.evaluate_game(game, player)
                    player.unplayed_wall_count = player.unplayed_wall_count + 1
                    game.unset_wall(x, y, side)                
                        

    def evaluate_game(self, game, player, moved=False):
        p1 = game.players[0]   
        p2 = game.players[1]
        #sp1 = len(self.find_shortest_path(p1, game.board))-1
        #sp2 = len(self.find_shortest_path(p2, game.board))-1
        sp1 = self.get_distance(p1, game.board)
        sp2 = self.get_distance(p2, game.board)
        wc1 = p1.unplayed_wall_count
        wc2 = p2.unplayed_wall_count
        cp = game.current_player
        total1 = (-sp1+sp2)*2 +wc1-wc2
        total2 = (sp1-sp2)*2 -wc1+wc2
        if cp == 0:
            if moved == False:
                total1 = total1 + 1
        else:
            if moved == False:
                total2 = total2 + 1
        print "dist1=%s, dist2=%s, wall1=%s, wall2=%s, current=%s => %s %s" \
            % (sp1, sp2, wc1, wc2, cp, total1, total2)  
                        
    
    def print_path(self, path):
        for space in path:
            sys.stdout.write(str(space))
        print ""
            
    def print_board(self, game):
        for x in range(9):
            for y in range(9):                    
                space = game.board.get(x,y)
                print str(x) + "," + str(y) + " " + str(space.occupied_by_player)
            
                