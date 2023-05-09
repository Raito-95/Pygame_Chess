class Player:
    def __init__(self, color):
        self.color = color
        self.captured_pieces = []

    def capture_piece(self, piece):
        self.captured_pieces.append(piece)
        
    # Add more player-related attributes or methods here
