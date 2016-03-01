import sys
from random import randint
from Space import Space
from GameEvent import GameEvent
from Logger import log

class AI:

    def __init__(self, game):
        self._game = game.clone()


    def determine_next_move(self, p):
        log("determine_next_move for " + str(p))
        game = self._game
        player = game.players[p.number]
        
        other_player = game.players[0]
        if p.number == 0:
            other_player = game.players[1]
        player_distance = game.board.get_distance(player.position, player.win_row)
        other_player_distance = game.board.get_distance(other_player.position, other_player.win_row)

        best_total = -99
        game_event = GameEvent("SPACE")

        should_try_wall = randint(0,game.turn)        
        log("try wall?", "wall count=", player.unplayed_wall_count, "turn=", self._game.turn, "should_try_wall=", should_try_wall)
        if player.unplayed_wall_count > 0 and game.turn > 1 and (game.turn > 3 or should_try_wall > 0 or other_player_distance < 4):
            best_total, game_event = self.propose_next_wall(game, player)

        path = self.find_shortest_path(player, game.board)
        if path != None and len(path) > 1:            
            next_space = path[1]
            moved = game.move_player(player, next_space.x, next_space.y)
            if moved:
                total = self.evaluate_game(game, player, True)
            else:
                log("determine_next_move: not moving", next_space.x, next_space.y)
                total = -99
            log("other player distance=", other_player_distance)
            log("best total from walls=" + str(best_total))
            log("move_total=" + str(total))
            if (total > 0 and player_distance < other_player_distance) or (total > best_total and best_total == -99) or (total >= best_total and other_player_distance >= 4):
                best_total = total
                game_event = GameEvent("SPACE")
                space = path[1]
                game_event.x = space.x
                game_event.y = space.y
                game_event.section = "CENTER"
                game_event.move_mode = "PAWN"
        return game_event

    def propose_next_wall(self, game, player):
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
        return (best_total, game_event)


    def find_shortest_path(self, player, board):
        log("find_shortest_path for " + str(player))
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
        log("dist1=%s, dist2=%s, wall1=%s, wall2=%s, moved=%s, current=%s => %s" \
            % (sp1, sp2, wc1, wc2, moved, cp, total))
        # check for possible jump
        if moved and p1.position.x == p2.position.x:
            y_dist = abs(p1.position.y - p2.position.y)
            if y_dist % 2 == 1 and p1.position.y < p2.position.y:
                log("subtracting from total")
                total = total - 1
            else:
                log("adding to total")
                total = total + 1
        return total
                        
    # TODO: log
    def print_path(self, path):
        for space in path:
            sys.stdout.write(str(space))
        print ""
            

                