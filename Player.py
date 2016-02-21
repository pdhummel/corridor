class Player:

    
    def __init__(self):
        self.name = None
        self.color = None
        self.is_computer = False
        self.unplayed_wall_count = 0
        self.position = None
        self.move_mode = None # PAWN, WALL
        self.win_row = None
        self.win_col = None
        self.number = -1        
    
    def clone(self):
        p = Player()
        p.name = self.name
        p.color = self.color
        p.is_computer = self.is_computer
        p.unplayed_wall_count = self.unplayed_wall_count
        p.move_mode = self.move_mode
        p.win_row = self.win_row
        p.win_col = self.win_col
        #p.position = self.position 
        p.number = self.number
        return p
        
    def __str__(self):
        return self.name + "," + str(self.number) + ", winX=" + str(self.win_col) + ", winY=" + str(self.win_row)
