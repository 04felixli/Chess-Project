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
    
    # generate all possible moves for a knight
    def allKnightMoves(self, clicks, DIMENSION):
        currentRow = clicks[0] # row the knight is on before being moved
        currentColumn = clicks[1] # column the knight is on before being moved

        # All possible vertical and horizontal movements of knight: eg.(verticalMoves[0], horizontalMoves[0])
        verticalMoves = [-2, -2, -1, -1, 1, 1, 2, 2]
        horizontalMoves = [-1, 1, -2, 2, 2, -2, -1, 1]

        # add up to 8 possibilities of moves for a knight
        for i in range(8):
            # Calculate the new position of the knight
            destinationRow = currentRow + verticalMoves[i]
            destinationColumn = currentColumn + horizontalMoves[i]

            # Check if the new position is on the board
            if 0 <= destinationRow < DIMENSION and 0 <= destinationColumn < DIMENSION:
                self.addMove(destinationRow, destinationColumn, currentRow, currentColumn)
    
    # generate all possible moves for a bishop
    def allBishopMoves(self, clicks, DIMENSION):
        currentRow = clicks[0] # row the bishop is on before being moved
        currentColumn = clicks[1] # column the bishop is on before being moved

        # Bishop can move in 4 directions, represented by a tuple: eg. down and right = (1, 1)
        diagonalMoves = [(1, 1), (-1, -1), (-1, 1), (1, -1)]

        for move in diagonalMoves:
            for i in range(1, DIMENSION): # i represents how many diagonal squares the bishop travels up to a max of 8 
                                          # (from one corner to the opposite corner is 8 squares)
                # Calculate the new position of the bishop
                destinationRow = currentRow + move[0] * i
                destinationColumn = currentColumn + move[1] * i

                # Check if the new position is on the board
                if 0 <= destinationRow < DIMENSION and 0 <= destinationColumn < DIMENSION:
                    self.addMove(destinationRow, destinationColumn, currentRow, currentColumn)

                    if self.checkPieceInPath(destinationRow, destinationColumn) == True: # if there is a piece in the path, stop going in this direction
                        break
                else: # if the bishop goes off the map, stop going in this direction
                    break

    # generate all possible moves for a rook
    def allRookMoves(self, clicks, DIMENSION):
        currentRow = clicks[0] # row the rook is on before being moved
        currentColumn = clicks[1] # column the rook is on before being moved

        # rook can move horizontally or vertically, but not diagonally
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for move in moves:
            for i in range(1, DIMENSION):
                # Calculate the new position of the rook
                destinationRow = currentRow + move[0] * i
                destinationColumn = currentColumn + move[1] * i

                # Check if the new position is on the board
                if 0 <= destinationRow < DIMENSION and 0 <= destinationColumn < DIMENSION:
                    self.addMove(destinationRow, destinationColumn, currentRow, currentColumn)
                    if self.checkPieceInPath(destinationRow, destinationColumn) == True: # if there is a piece in the path, stop going in this direction
                        break
                else: # if the bishop goes off the map, stop going in this direction
                    break

    def allKingMoves(self, clicks, DIMENSION):
        currentRow = clicks[0] # row the rook is on before being moved
        currentColumn = clicks[1] # column the rook is on before being moved

        moves = [(-1, -1), (-1, 1), (1, 1), (1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]

        for move in moves:
            destinationRow = currentRow + move[0]
            destinationColumn = currentColumn + move[1]
            # Check if the new position is on the board
            if 0 <= destinationRow < DIMENSION and 0 <= destinationColumn < DIMENSION:
                self.addMove(destinationRow, destinationColumn, currentRow, currentColumn)

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

    # check if the piece in the way is the same color as the piece being moved 
    def checkSameColor(self, destinationRow, destinationColumn, currentRow, currentColumn):
        pieceToMove = self.board[destinationRow][destinationColumn]
        pieceToReplace = self.board[currentRow][currentColumn]

        # if the pieces are different colors, the pieceToMove can replace the pieceToReplace
        if pieceToMove[0] != pieceToReplace[0]:
            return False
        else:
            return True
        






    
