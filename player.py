class Player:
    def __init__(self, color):
        self.color = color
        self.captured = []

    def captured_history(self, piece):
        self.captured.append(piece)