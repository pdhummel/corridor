from Space import Space

class Board:
	
    def __init__(self):	
        self.spaces = [[None for col in range(9)] for row in range(9)]
	
    def initialize(self):	
        for x in range(9):
            for y in range(9):
                space = Space()
                space.x = x
                space.y = y
                self.set(x, y, space)
                	
                

    def clone(self):
        b = Board()
        for x in range(9):
            for y in range(9): 
                space = self.get(x, y)    
                s = space.clone()
                b.set(x, y, s)
        return b
        

    def get(self, x, y):
        return self.spaces[x][y]
        
    def set(self, x, y, space):
        self.spaces[x][y] = space
    
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

