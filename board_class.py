# This file handles game logic including:
#   - The current state of the board

class Board:
    def __init__(self):
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],  # Stores the location of all pieces on a 8x8 board using a 2D array 
                    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],    # bR denotes "black rook" and wR denotes "white rook"
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.whiteTurn = True
        self.blackKingLocation = ()

    
