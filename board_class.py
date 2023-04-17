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
        self.stuckPieces = [] # a list of all pieces that if moved, will result in the king of the same color being in check

    # generate all possible moves for a pawn 
    def allPawnMoves(self, currentRow, currentColumn, DIMENSION):
        # currentRow = clicks[0] # row the pawn is on before being moved
        # currentColumn = clicks[1] # column the pawn is on before being moved
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
    def allKnightMoves(self, currentRow, currentColumn, DIMENSION):
        # currentRow = clicks[0] # row the knight is on before being moved
        # currentColumn = clicks[1] # column the knight is on before being moved

        # All possible vertical and horizontal movements of knight: eg.(verticalMoves[0], horizontalMoves[0])
        verticalMoves = [-2, -2, -1, -1, 1, 1, 2, 2]      
        horizontalMoves = [-1, 1, -2, 2, 2, -2, -1, 1]

        # knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1)]

        # add up to 8 possibilities of moves for a knight
        for i in range(8):
            # Calculate the new position of the knight
            destinationRow = currentRow + verticalMoves[i]
            destinationColumn = currentColumn + horizontalMoves[i]

            # Check if the new position is on the board
            if 0 <= destinationRow < DIMENSION and 0 <= destinationColumn < DIMENSION:
                self.addMove(destinationRow, destinationColumn, currentRow, currentColumn)
    
    # generate all possible moves for a bishop
    def allBishopMoves(self, currentRow, currentColumn, DIMENSION):
        # currentRow = clicks[0] # row the bishop is on before being moved
        # currentColumn = clicks[1] # column the bishop is on before being moved

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
    def allRookMoves(self, currentRow, currentColumn, DIMENSION):
        # currentRow = clicks[0] # row the rook is on before being moved
        # currentColumn = clicks[1] # column the rook is on before being moved

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

    # generate all possible moves for a king
    def allKingMoves(self, currentRow, currentColumn, DIMENSION):
        # currentRow = clicks[0] # row the rook is on before being moved
        # currentColumn = clicks[1] # column the rook is on before being moved

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
        pieceToMove = self.board[currentRow][currentColumn]
        pieceToReplace = self.board[destinationRow][destinationColumn]

        # if the pieces are different colors, the pieceToMove can replace the pieceToReplace
        if pieceToMove[0] != pieceToReplace[0]:
            return False
        else:
            return True
    
    # checks who's turn it is
    def checkValidTurn(self, clicks):
        currentRow = clicks[0] # row the piece is on before being moved
        currentColumn = clicks[1] # column the piece is on before being moved
        destinationRow = clicks[2]
        destinationColumn = clicks[3]
        pieceToMove = self.board[currentRow][currentColumn]
        destination = self.board[destinationRow][destinationColumn] 
        pieceMovedColor = pieceToMove[0]
        destinationColor = destination[0]

        # returns true if the piece being moved is the correct color, false otherwise
        if ((pieceMovedColor == 'w' != destinationColor) and self.whiteTurn == True) or ((pieceMovedColor == 'b' != destinationColor) and self.whiteTurn == False):
            return True
        else:
            return False

    # checks if a piece can move to a certain location
    def checkValidMove(self, clicks, DIMENSION):
        pieceClickedOn = self.board[clicks[0]][clicks[1]][1]
        destination = (clicks[2], clicks[3])

        if pieceClickedOn not in self.stuckPieces:
            self.generateAllValidMovesForPiece(clicks[0], clicks[1], pieceClickedOn, DIMENSION)
            
            if destination in self.validMoves:
                self.validMoves.clear()
                return True
            else:
                return False
        else: 
            return False
        
    # generates all valid moves for a piece at it's currentRow and currentColumn
    def generateAllValidMovesForPiece(self, currentRow, currentColumn, piece, DIMENSION):
        if piece == 'P':
            self.allPawnMoves(currentRow, currentColumn, DIMENSION)
        elif piece == 'N':
            self.allKnightMoves(currentRow, currentColumn, DIMENSION)
        elif piece == 'B':
            self.allBishopMoves(currentRow, currentColumn, DIMENSION)
        elif piece == 'R':
            # bs.allRookMoves(clicks, DIMENSION)
            self.allRookMoves(currentRow, currentColumn, DIMENSION)
        elif piece == 'Q':
            self.allRookMoves(currentRow, currentColumn, DIMENSION)
            self.allBishopMoves(currentRow, currentColumn, DIMENSION)
        elif piece == 'K':
            self.allKingMoves(currentRow, currentColumn, DIMENSION)

    # checks if a move made by a color results in the same color king being in check
    # checks if a move made by the opposing color results in check 
    def checkCheck(self, DIMENSION):
        
        # need to check up, down, right, left, up left, up right, down right, down left, 
        # for knights that can check the king, just pretend king is a knight and generate all moves for it

        pathsToKing = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (1, 1), (-1, 1), 
                       (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1)]

        if self.whiteTurn == False: # if it's black's turn to move, need to check if black king is in check by white pieces
            currentRow = self.blackKingLocation[0]
            currentColumn = self.blackKingLocation[1]
            rowOfPawnCheck = 1 # The only way for a white pawn to check the black king is if it is the row "below" the king
        else: 
            currentRow = self.whiteKingLocation[0]
            currentColumn = self.whiteKingLocation[1]
            rowOfPawnCheck = -1 # The only way for a white pawn to check the black king is if it is the row "above" the king

        for path in pathsToKing:
            for i in range(1, DIMENSION):

                if path[0] == 2 or path[1] == 2 or path[0] == -2 or path[1] == -2: # look for checking knights
                    destinationRow = currentRow + path[0]
                    destinationColumn = currentColumn + path[1]
                else:
                    destinationRow = currentRow + path[0] * i 
                    destinationColumn = currentColumn + path[1] * i

                # Check if the new position is on the board
                if 0 <= destinationRow < DIMENSION and 0 <= destinationColumn < DIMENSION:
                    # check if there is a piece that has line of sight to the king  
                    if self.checkPieceInPath(destinationRow, destinationColumn) == True:

                        print("Piece in path")

                        # check if the piece is a different color 
                        if self.checkSameColor(destinationRow, destinationColumn, currentRow, currentColumn) == False:

                            print("Piece is different color")

                            pieceInWay = self.board[destinationRow][destinationColumn][1]
                            if path[0] == 0 or path[1] == 0: # check if a rook or queen has vertical or horizontal line of sight to king
                                if pieceInWay == 'R' or pieceInWay == 'Q':
                                    print("Check by rook or Queen")
                                    return True
                                else: # if the piece in the way is not a rook or queen, move to next direction
                                    break 
                            elif path[0] == 2 or path[1] == 2 or path[0] == -2 or path[1] == -2:
                                if pieceInWay == 'N':
                                    print("check by knight")
                                    return True
                                else:
                                    break
                            else: # check if a bishop or queen or pawn has diagonal line of sight to king
                                if pieceInWay == 'B' or pieceInWay == 'Q':
                                    print("check by bishop or queen")
                                    return True
                                elif pieceInWay == 'P' and currentRow + rowOfPawnCheck == destinationRow: # check if a pawn of the opposite color is in the appropriate row to check the king
                                    print("check by pawn")
                                    return True
                                else: # if the piece in the way is not a bishop or queen, move to next direction
                                    break
                        else: # if the piece in the way is of the same color, move in another direction
                            break
                else:
                    break # stop from going off board in a direction
        
        return False
                        
                            
                        

        





    
