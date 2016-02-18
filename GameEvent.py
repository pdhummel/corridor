class GameEvent:

    
    
    def __init__(self, event_name):
        # NOOP, EXIT, SPACE, TOP, BOTTOM, LEFT, RIGHT
        self.name = event_name
        self.section = None
        self.x = -1
        self.y = -1    
        
        