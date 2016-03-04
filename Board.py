from Space import Space
from Logger import log

class Board:

    def __init__(self):
        self.spaces = [[None for col in range(9)] for row in range(9)]
        self.graph = {}
        self.space_distances_p1 = {}
        self.space_distances_p2 = {}


    def initialize(self):	
        for x in range(9):
            for y in range(9):
                space = Space()
                space.x = x
                space.y = y
                self.set(x, y, space)

        self.graph = self.create_graph()
        self.space_distances_p1 = self.calculate_space_distances(self.graph, 8)
        self.space_distances_p2 = self.calculate_space_distances(self.graph, 0)

    def clone(self):
        b = Board()
        for x in range(9):
            for y in range(9): 
                space = self.get(x, y)
                s = space.clone()
                b.set(x, y, s)

        for x in range(9):
            for y in range(9): 
                space = self.get(x, y)
                s = b.get(x, y)
                if self.space_distances_p1.has_key(space):
                    b.space_distances_p1[s] = self.space_distances_p1[space]
                if self.space_distances_p2.has_key(space):
                    b.space_distances_p2[s] = self.space_distances_p2[space]
                if self.graph.has_key(space):
                    cells = []
                    for node in self.graph[space]:
                        cell = b.get(node.x, node.y)
                        cells.append(cell)
                    b.graph[s] = cells
        return b

    def board_changed(self):
        log("board_changed")
        new_graph = self.create_graph()
        self.graph = new_graph
        self.space_distances_p1 = self.calculate_space_distances(self.graph, 8)
        self.space_distances_p2 = self.calculate_space_distances(self.graph, 0)



    def get(self, x, y):
        return self.spaces[x][y]
        
    def set(self, x, y, space):
        self.spaces[x][y] = space
    
    def create_graph(self):
        log("create_graph")
        board = self
        graph = {}
        for x in range(9):
            for y in range(9): 
                space = board.get(x, y)  
                to_cells = []
                if y > 0 and space.top_has_wall == False:
                    top = board.get(x, y-1)
                    if top.bottom_has_wall == False:
                        to_cells.append(top)
                    # TODO:  diaganol pawn jump
                    if top.occupied_by_player != None:
                        if top.y > 1 and top.top_has_wall == False:
                            top = board.get(x, y-2)
                            to_cells.append(top)
                if y < 8 and space.bottom_has_wall == False:
                    bottom = board.get(x, y+1)
                    if bottom.top_has_wall == False:
                        to_cells.append(bottom)
                    # TODO:  diaganol pawn jump
                    if bottom.occupied_by_player != None:
                        if bottom.y < 7 and bottom.bottom_has_wall == False:
                            bottom = board.get(x, y+2)
                            to_cells.append(bottom)
                if x > 0 and space.left_has_wall == False:
                    left = board.get(x-1, y)
                    if left.right_has_wall == False:
                        to_cells.append(left)
                    # TODO:  diaganol pawn jump
                    if left.occupied_by_player != None:
                        if left.x > 1 and left.left_has_wall == False:
                            left = board.get(x-2, y)
                            to_cells.append(left)
                if x < 8 and space.right_has_wall == False:
                    right = board.get(x+1, y)
                    if right.left_has_wall == False:
                        to_cells.append(right) 
                    # TODO:  diaganol pawn jump
                    if right.occupied_by_player != None:
                        if right.x < 7 and right.right_has_wall == False:
                            right = board.get(x+2, y)
                            to_cells.append(right)
                graph[space] = to_cells
        return graph

    def output_graph(self, graph):
        for x in range(9):
            for y in range(9):
                space = self.get(x, y)
                if graph.has_key(space):
                    log(x, y, "->", graph[space])
                else:
                    log(x, y, "->", None)


    def get_distance(self, space, victory_row):
        graph = self.graph
        if victory_row == 8:
            space_distances = self.space_distances_p1
        else:
            space_distances = self.space_distances_p2        
        distance = -1
        if space_distances.has_key(space):
            distance = space_distances[space]
        return distance


    # Check if the space is connected to the victory row.
    def is_connected(self, space, victory_row):
        log("is_connected")
        connected = False
        graph = self.graph
        connected_spaces = self.find_connected_spaces(graph, victory_row)
        if space in connected_spaces:
            connected = True
        del connected_spaces[:]
        return connected

    def find_connected_spaces(self, graph, victory_row):
        log("find_connected_spaces for row ", victory_row)
        if victory_row == 8:
            space_distances = self.space_distances_p1
        else:
            space_distances = self.space_distances_p2
        connected_spaces = space_distances.keys()
        return connected_spaces

    def calculate_space_distance(self, graph, victory_row, space_distances, x, y):
        space = self.get(x, y)        
        if y == victory_row:
            space_distances[space] = 0

        # Try to get the distance for this space from its nodes
        elif graph.has_key(space) and (space_distances.has_key(space)):
            for node in graph[space]:
                if graph.has_key(node) and space_distances.has_key(node):
                    distance = space_distances[node]
                    if space_distances[space] > distance+1:
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
                    self.calculate_space_distance(graph, victory_row, space_distances, node.x, node.y)

    def calculate_space_distances(self, graph, victory_row):
        log("calculate_space_distances")
        space_distances = {}
        y = victory_row

        # We need to loop just in case the cols in the victory row have walls between them.
        for col in range(9):
            x = col
            self.calculate_space_distance(graph, victory_row, space_distances, x, y)
        self.calculate_space_distance(graph, victory_row, space_distances, 0, 0)
        self.calculate_space_distance(graph, victory_row, space_distances, 8, 8)

        # Return here to turn-off output of space_distances
        return space_distances
        for row in range(9):
            output = ""
            for col in range(9):
                x = col
                y = row
                space = self.get(x,y)
                if space_distances.has_key(space):
                    output = output + " " + str(space_distances[space])
                else:
                    output = output + " ?"
            log(output)
        log(" ")
        return space_distances

    # TODO: redo this output using the ConsoleInterface code
    def __str__(self):
        output = ""
        for y in range(9):
            row_output = ""
            for x in range(9):
                space = self.get(x, y)
                if space.top_has_wall:
                    row_output = row_output + "T"
                else:
                    row_output = row_output + "t"
                if space.right_has_wall:
                    row_output = row_output + "R"
                else:
                    row_output = row_output + "r"
                if space.bottom_has_wall:
                    row_output = row_output + "B"
                else:
                    row_output = row_output + "b"
                if space.left_has_wall:
                    row_output = row_output + "L"
                else:
                    row_output = row_output + "l"
                if space.occupied_by_player != None:
                    row_output = row_output + "P"
                else:
                    row_output = row_output + "p"
                row_output = row_output + " "

            row_output = row_output + "\n"
            output = output + row_output
        output = output + "\n"
        return output
