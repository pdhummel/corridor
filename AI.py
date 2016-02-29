import sys
from Space import Space
from GameEvent import GameEvent

class AI:

    def __init__(self, game):
        self._game = game.clone()
    

        

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

    def find_shortest_path(self, player, board):
        print "find_shortest_path for " + str(player)
        graph = board.create_graph()
        start = player.position
        end = board.get(0, player.win_row)
        path = []
        shortest_path = self.find_shortest_path2(graph, start, end, path)
        return shortest_path


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


    def evaluate_game(self, game, player, moved=False):
        p1 = game.players[0]   
        p2 = game.players[1]
        if p1.name == player.name:
            p1.unplayed_wall_count = player.unplayed_wall_count
        else:
            p2.unplayed_wall_count = player.unplayed_wall_count
        sp1 = game.board.get_distance(p1.position, p1.win_row)
        sp2 = game.board.get_distance(p2.position, p2.win_row)
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
            

                