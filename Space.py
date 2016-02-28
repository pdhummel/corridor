class Space:
    
    def __init__(self):
        self.occupied_by_player = None
        self.top_has_wall = False
        self.bottom_has_wall = False
        self.left_has_wall = False
        self.right_has_wall = False
        self.x = -1
        self.y = -1
            
    def clone(self):
        s = Space()
        s.top_has_wall = self.top_has_wall
        s.bottom_has_wall = self.bottom_has_wall
        s.left_has_wall = self.left_has_wall
        s.right_has_wall = self.right_has_wall
        s.x = self.x
        s.y = self.y
        s.occupied_by_player = self.occupied_by_player
        return s
        
    def __str__(self):
        return str(self.x) + "," + str(self.y) + " " #+ \
    #       ":  top=" + str(self.top_has_wall) + \
    #       ", bottom=" + str(self.bottom_has_wall) + \
    #       ", left=" + str(self.left_has_wall) + \
    #       ", right=" + str(self.right_has_wall) + " " 