from Space import Space

class Board:
	
    def __init__(self):	
        #self.spaces = {}
        self.spaces = [[None for col in range(9)] for row in range(9)]
        #pass
	
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
                #b.spaces[str(x)+","+str(y)] = s
                #print "spaces:  " + str(space) + " " + str(s) 
                #print "    bs:  " + str(self.get(x,y)) + " " + str(b.get(x,y))
                #print "    bs:  " + str(self.get(x,y)) + " " + str(b.spaces[str(x)+","+str(y)])
        return b
        

    def get(self, x, y):
        return self.spaces[x][y]
        #return self.spaces[str(x)+","+str(y)]
        
    def set(self, x, y, space):
        self.spaces[x][y] = space
        #self.spaces[str(x)+","+str(y)] = space
    