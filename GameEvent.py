class GameEvent:

    
    
    def __init__(self, event_name):
        # NOOP, EXIT, SPACE, TOP, BOTTOM, LEFT, RIGHT
        self.name = event_name
        self.section = None
        self.x = -1
        self.y = -1
        self.move_mode = None
        
    def __str__(self):
        return str(self.name) + "," + str(self.section) + ": " + str(self.x) + "," + str(self.y) + " " + str(self.move_mode)
