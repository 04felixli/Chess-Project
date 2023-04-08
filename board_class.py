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
        self.blackKingLocation = (0, 4) 
        self.whiteKingLocation = (7, 4)
        self.validMoves = [] # a list of all possible valid moves at a certain colors turn for the piece clicked on

    # generate all possible moves for a pawn 
    def allPawnMoves(self, clicks, DIMENSION):
        currentRow = clicks[0] # row the pawn is on before being moved
        currentColumn = clicks[1] # column the pawn is on before being moved
        pieceToMove = self.board[currentRow][currentColumn] 
        pieceColor = pieceToMove[0]
        destinationRow = currentRow

        # left diagonal, up one, right diagonal
        for i in range(-1, 2):
            destinationColumn = currentColumn + i

            if currentRow - 1 >= 0 and currentRow + 1 < DIMENSION: # check piece will still be in board
                if pieceColor == 'w':
                    destinationRow = currentRow - 1
                else: 
                    destinationRow = currentRow + 1

            # if pieceColor == 'w':
            #     if currentRow - 1 >= 0: # check piece will still be in board
            #         destinationRow = currentRow - 1
            # else:
            #     if currentRow + 1 < DIMENSION: # check piece will still be in board
            #         destinationRow = currentRow + 1

            if destinationColumn == currentColumn: # move up one square 
                    if self.checkPieceInPath(destinationRow, destinationColumn) == False: # pawn cannot take moving forward
                        self.validMoves.append((destinationRow, destinationColumn))
            elif destinationColumn >= 0 and destinationColumn < DIMENSION and currentRow != 0 and currentRow != 7: # move left diagonal up or right diagonal up, check piece will still be in board.
                                                                                                                   # and make sure pawn is not at the other end of the board because then it cannot move
                if self.checkPieceInPath(destinationRow, destinationColumn) == True and self.checkSameColor(destinationRow, destinationColumn, currentRow, currentColumn) == False:
                    self.validMoves.append((destinationRow, destinationColumn))

        # pawns can also move two squares up if there is nothing there and they have not been moved yet
        if pieceColor == 'w' and currentRow == 6:
            if self.checkPieceInPath(currentRow - 2, currentColumn) == False: 
                self.validMoves.append((currentRow - 2, currentColumn))

        if pieceColor == 'b' and currentRow == 1:
            if self.checkPieceInPath(currentRow + 2, currentColumn) == False:
                self.validMoves.append((currentRow + 2, currentColumn))
            



        

        
        
        


    def addMove(self, destinationRow, destinationColumn, currentRow, currentColumn):
        # check if there is a piece in the way
        if self.checkPieceInPath(destinationRow, destinationColumn):
            # if there is a piece in the way, check its color
            # If it is the same, cannot go there so do not append to list. If it is different, can go there, so append list

            if self.checkSameColor(destinationRow, destinationColumn, currentRow, currentColumn) == False:
                self.validMoves.append((destinationRow, destinationColumn))
        else:
            self.validMoves.append((destinationRow, destinationColumn))

    # check if there is a piece in the way
    def checkPieceInPath(self, destinationRow, destinationColumn):
        if self.board[destinationRow][destinationColumn] != '..':
            return True
        else:
            return False

    def checkSameColor(self, destinationRow, destinationColumn, currentRow, currentColumn):
        pieceToMove = self.board[destinationRow][destinationColumn]
        pieceToReplace = self.board[currentRow][currentColumn]

        # if the pieces are different colors, the pieceToMove can replace the pieceToReplace
        if pieceToMove[0] != pieceToReplace[0]:
            return False
        else:
            return True
        






    
