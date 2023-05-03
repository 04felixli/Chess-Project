# This file handles game logic including:
#   - The current state of the board

class Board:
    def __init__(self):
        # self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],  # Stores the location of all pieces on a 8x8 board using a 2D array 
        #             ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],    # bR denotes "black rook" and wR denotes "white rook"
        #             ['..', '..', '..', '..', '..', '..', '..', '..'],
        #             ['..', '..', '..', '..', '..', '..', '..', '..'],
        #             ['..', '..', '..', '..', '..', '..', '..', '..'],
        #             ['..', '..', '..', '..', '..', '..', '..', '..'],
        #             ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        #             ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.board = [['..', '..', '..', '..', 'bK', '..', '..', '..'],  # Stores the location of all pieces on a 8x8 board using a 2D array 
                    ['wR', '..', '..', '..', '..', '..', '..', '..'],    # bR denotes "black rook" and wR denotes "white rook"
                    ['..', '..', '..', '..', '..', '..', 'wR', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', 'wK', '..', '..', '..']]

        self.whiteTurn = True
        self.blackKingLocation = (0, 4) 
        self.whiteKingLocation = (7, 4)
        self.validMoves = [] # a list of all possible valid moves at a certain colors turn for the piece clicked on
        self.attackingPieces = [] # a list of all pieces that attack a certain square
        self.checkingPieces = [] # a list of all checking pieces
        self.kingMoves = [] # a list of all moves a king can make 
        

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
                else: # if the rook goes off the map, stop going in this direction
                    break

    # generate all possible moves for a king
    def allKingMoves(self, currentRow, currentColumn, DIMENSION):
        self.kingMoves.clear()
        # keep track of what row and column the king is on 
       
        king = self.board[currentRow][currentRow]

        moves = [(-1, -1), (-1, 1), (1, 1), (1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]

        for move in moves:
            destinationRow = currentRow + move[0]
            destinationColumn = currentColumn + move[1]
            # Check if the new position is on the board and that the new position is not attacked by other pieces
            if 0 <= destinationRow < DIMENSION and 0 <= destinationColumn < DIMENSION:
                if self.checkSameColor(destinationRow, destinationColumn, currentRow, currentColumn) == False:
                    # temp move king to destination square
                    temp = self.board[currentRow][currentColumn] 
                    self.board[currentRow][currentColumn] = '..'
                    pieceTaken = self.board[destinationRow][destinationColumn]
                    self.board[destinationRow][destinationColumn] = temp

                    # check if the square the king just moved to is not attacked, if it is not, the king can move there
                    if self.squareAttacked(destinationRow, destinationColumn, DIMENSION) == False:
                        self.validMoves.append((destinationRow, destinationColumn))
                        self.kingMoves.append((destinationRow, destinationColumn))
                    
                    # move the king back to current square
                    
                    self.board[currentRow][currentColumn] = self.board[destinationRow][destinationColumn]
                    self.board[destinationRow][destinationColumn] = pieceTaken

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

        self.generateAllValidMovesForPiece(clicks[0], clicks[1], pieceClickedOn, DIMENSION)
        
        if destination in self.validMoves:
            self.validMoves.clear()
            return True
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

    # checks if the king is in check
    # keeps track of checking pieces
    def check(self, DIMENSION):

        self.checkingPieces.clear()

        if self.whiteTurn == True:
            kingRow = self.whiteKingLocation[0]
            kingColumn = self.whiteKingLocation[1]
            opposingColor = 'b'
        else:
            kingRow = self.blackKingLocation[0]
            kingColumn = self.blackKingLocation[1]
            opposingColor = 'w'
        
        # directions for each type of piece
        # checkPawns is the same as checkBishop
        # checkQueen use both checkRooks and checkBishops
        checkRooks = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        checkBishops = [(1, 1), (-1, -1), (1, -1), (-1, 1)] 
        checkKnights = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1)]

        # check for rooks and queens
        for direction in checkRooks:
            for i in range(1, DIMENSION):
                rowToCheck = kingRow + direction[0]*i
                columnToCheck = kingColumn + direction[1]*i

                # Check if the new position is on the board
                if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                    # if we find a rook or queen of the opposing color, add it to checkingPieces
                    if ((self.board[rowToCheck][columnToCheck][1] == 'R') or (self.board[rowToCheck][columnToCheck][1] == 'Q')) and (self.board[rowToCheck][columnToCheck][0] == opposingColor):
                        self.checkingPieces.append((rowToCheck, columnToCheck))
                    elif self.board[rowToCheck][columnToCheck] == '..': # continue in the same direction if the square is empty
                        pass
                    else: # go to next direction if the square is occupied by the same color piece
                        break
                else: # go to next direction if we go off board
                    break
        
        # check for bishops and queens 
        for direction in checkBishops:
            for i in range(1, DIMENSION):
                rowToCheck = kingRow + direction[0]*i
                columnToCheck = kingColumn + direction[1]*i
                
                # Check if the new position is on the board
                if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                    # if we find a bishop or queen of the opposing color, add it to checkingPieces
                    if ((self.board[rowToCheck][columnToCheck][1] == 'B') or (self.board[rowToCheck][columnToCheck][1] == 'Q')) and (self.board[rowToCheck][columnToCheck][0] == opposingColor):
                        self.checkingPieces.append((rowToCheck, columnToCheck))
                    elif self.board[rowToCheck][columnToCheck] == '..': # continue in the same direction if the square is empty
                        pass
                    else: # go to next direction if the square is occupied by the same color piece
                        break
                else:
                    break
        
        # check for knights 
        for direction in checkKnights:
            rowToCheck = kingRow + direction[0]
            columnToCheck = kingColumn + direction[1]
            # Check if the new position is on the board
            if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                # if we find a knight of the opposing color, add it to checkingPieces
                if self.board[rowToCheck][columnToCheck][1] == 'N' and self.board[rowToCheck][columnToCheck][0] == opposingColor:
                    self.checkingPieces.append((rowToCheck, columnToCheck))
            
        
        # check for pawns
        if opposingColor == 'w':
            if 0 <= kingRow + 1 < DIMENSION and 0 <= kingColumn + 1 < DIMENSION and self.board[kingRow + 1][kingColumn + 1] == 'wP':
                self.checkingPieces.append((kingRow + 1, kingColumn + 1))
            elif 0 <= kingRow + 1 < DIMENSION and 0 <= kingColumn - 1 < DIMENSION and self.board[kingRow + 1][kingColumn - 1] == 'wP':
                self.checkingPieces.append((kingRow + 1, kingColumn - 1))
        else:
            if 0 <= kingRow - 1 < DIMENSION and 0 <= kingColumn - 1 < DIMENSION and self.board[kingRow - 1][kingColumn - 1] == 'bP':
                self.checkingPieces.append((kingRow - 1, kingColumn - 1))
            elif 0 <= kingRow - 1 < DIMENSION and 0 <= kingColumn + 1 < DIMENSION and self.board[kingRow - 1][kingColumn + 1] == 'bP':
                self.checkingPieces.append((kingRow - 1, kingColumn + 1))

        # if there are no checking pieces, not check, else it is check
        if len(self.checkingPieces) == 0:
            return False
        else:
            return True

    def checkmate(self, DIMENSION):
        # check if king is in check 
        if self.check(DIMENSION):
            print("The king is in Check")
            # check if the king can move out of check

            if self.whiteTurn:
                kingRow = self.whiteKingLocation[0]
                kingColumn = self.whiteKingLocation[1]
            else:
                kingRow = self.blackKingLocation[0]
                kingColumn = self.blackKingLocation[1]

            self.allKingMoves(kingRow, kingColumn, DIMENSION)

            if self.kingMoves != []: # if the king can move, it is not checkmate
                print("The king can move out of check")
                return False
            elif len(self.checkingPieces) == 2: # if the king cannot move and it is double check, it is checkmate
                print("It is a double check and the king cannot move")
                return True
            elif self.squareAttacked(self.checkingPieces[0][0], self.checkingPieces[0][1], DIMENSION) and self.kingMoves != []: # check if checking piece can be taken
                print("The checking piece can be taken")
                return False
            elif self.blockCheck(DIMENSION): # check if check can be blocked 
                print("The check can be blocked")
                return False
            else:
                return True
        else:
            return False

    # checks if a square is attacked 
    # only works if the square attacked corresponds to whose turn it is 
    # eg. if it is black's turn, can only check if black pieces are attacked by white pieces
    def squareAttacked(self, rowAttacked, columnAttacked, DIMENSION):
        
        # figure out what the opposing color is 
        if self.whiteTurn == True:
            opposingColor = 'b'
        else:
            opposingColor = 'w'
        
        # directions for types of pieces
        checkRooks = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        checkBishops = [(1, 1), (-1, -1), (1, -1), (-1, 1)] 
        checkKnights = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1)]

        # check for rooks and queens
        for direction in checkRooks:
            for i in range(1, DIMENSION):
                rowToCheck = rowAttacked + direction[0]*i
                columnToCheck = columnAttacked + direction[1]*i

                # Check if the new position is on the board
                if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                    # if we find a rook or queen of the opposing color, add it to checkingPieces
                    if ((self.board[rowToCheck][columnToCheck][1] == 'R') or (self.board[rowToCheck][columnToCheck][1] == 'Q')) and (self.board[rowToCheck][columnToCheck][0] == opposingColor):
                        return True
                    elif self.board[rowToCheck][columnToCheck] == '..': # continue in the same direction if the square is empty
                        pass
                    else: # go to next direction if the square is occupied by the same color piece
                        break
                else: # go to next direction if we go off board
                    break
        
        # check for bishops and queens 
        for direction in checkBishops:
            for i in range(1, DIMENSION):
                rowToCheck = rowAttacked + direction[0]*i
                columnToCheck = columnAttacked + direction[1]*i\
                
                # Check if the new position is on the board
                if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                    # if we find a bishop or queen of the opposing color, add it to checkingPieces
                    if ((self.board[rowToCheck][columnToCheck][1] == 'B') or (self.board[rowToCheck][columnToCheck][1] == 'Q')) and (self.board[rowToCheck][columnToCheck][0] == opposingColor):
                        return True 
                    elif self.board[rowToCheck][columnToCheck] == '..': # continue in the same direction if the square is empty
                        pass
                    else: # go to next direction if the square is occupied by the same color piece
                        break
                else:
                    break
        
        # check for knights 
        for direction in checkKnights:
            rowToCheck = rowAttacked + direction[0]
            columnToCheck = columnAttacked + direction[1]
            # Check if the new position is on the board
            if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                # if we find a knight of the opposing color, add it to checkingPieces
                if self.board[rowToCheck][columnToCheck][1] == 'N' and self.board[rowToCheck][columnToCheck][0] == opposingColor:
                    return True
            
        # check for pawns
        if opposingColor == 'w':
            if 0 <= rowAttacked + 1 < DIMENSION and 0 <= columnAttacked + 1 < DIMENSION and self.board[rowAttacked + 1][columnAttacked + 1] == 'wP':
                return True
            elif 0 <= rowAttacked + 1 < DIMENSION and 0 <= columnAttacked - 1 < DIMENSION and self.board[rowAttacked + 1][columnAttacked - 1] == 'wP':
                return True 
        else:
            if 0 <= rowAttacked - 1 < DIMENSION and 0 <= columnAttacked - 1 < DIMENSION and self.board[rowAttacked - 1][columnAttacked - 1] == 'bP':
                return True
            elif 0 <= rowAttacked - 1 < DIMENSION and 0 <= columnAttacked + 1 < DIMENSION and self.board[rowAttacked - 1][columnAttacked + 1] == 'bP':
                return True

        # check for kings
        for direction in checkRooks:
            rowToCheck = rowAttacked + direction[0]
            columnToCheck = columnAttacked + direction[1]
            # Check if the new position is on the board
            if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                # if we find a knight of the opposing color, add it to checkingPieces
                if self.board[rowToCheck][columnToCheck][1] == 'K' and self.board[rowToCheck][columnToCheck][0] == opposingColor:
                    return True
        for direction in checkBishops:
            rowToCheck = rowAttacked + direction[0]
            columnToCheck = columnAttacked + direction[1]
            # Check if the new position is on the board
            if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                # if we find a knight of the opposing color, add it to checkingPieces
                if self.board[rowToCheck][columnToCheck][1] == 'K' and self.board[rowToCheck][columnToCheck][0] == opposingColor:
                    return True

        return False

    # checks if a check can be blocked
    # 1. finds the direction of the checking piece relative to the king 
    # 2. checks if the squares in b/w can be taken by a piece of the same color as the king
    # BEWARE: at this point, checking pieces should only have one element in it since a double check cannot be blocked 
    def blockCheck(self, DIMENSION):
        
        # figure out what color is trying to block the check
        if self.whiteTurn == True:
            kingRow = self.whiteKingLocation[0]
            kingColumn = self.whiteKingLocation[1]
            blockingColor = 'w'
        else:
            kingRow = self.blackKingLocation[0]
            kingColumn = self.blackKingLocation[1]
            blockingColor = 'b'
        
        # get the location of the checking piece
        rowOfCheckPiece = self.checkingPieces[0][0]
        columnofCheckPiece = self.checkingPieces[0][1]
        checkingPiece = self.board[rowOfCheckPiece][columnofCheckPiece]

        # figure out which direction the checking piece is
        if checkingPiece[1] == 'Q' or checkingPiece[1] == 'B': # queen and bishop check
            if kingRow < rowOfCheckPiece and kingColumn < columnofCheckPiece:
                directionOfCheckPiece = (1, 1)
            elif kingRow > rowOfCheckPiece and kingColumn > columnofCheckPiece:
                directionOfCheckPiece = (-1, -1)
            elif kingRow < rowOfCheckPiece and kingColumn > columnofCheckPiece:
                directionOfCheckPiece = (1, -1)
            else:
                directionOfCheckPiece = (-1, 1)
        else: # rook and queen check
            if kingColumn < columnofCheckPiece:
                directionOfCheckPiece = (0, 1)
            elif kingColumn > columnofCheckPiece:
                directionOfCheckPiece = (0, -1)
            elif kingRow < rowOfCheckPiece:
                directionOfCheckPiece = (1, 0)
            else:
                directionOfCheckPiece = (-1, 0)

        # see if the squares b/w king and checking piece can be occupied 
        for i in range(1, DIMENSION):
            if kingRow + directionOfCheckPiece[0]*i < rowOfCheckPiece and kingColumn + directionOfCheckPiece[1]*i < columnofCheckPiece:
                rowBlock = kingRow + directionOfCheckPiece[0]*i
                columnBlock = kingColumn + directionOfCheckPiece[1]*i
        
                # directions for types of pieces
                checkRooks = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                checkBishops = [(1, 1), (-1, -1), (1, -1), (-1, 1)] 
                checkKnights = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1)]

                # check for rooks and queens
                for direction in checkRooks:
                    for k in range(1, DIMENSION):
                        rowToCheck = rowBlock + direction[0]*k
                        columnToCheck = columnBlock + direction[1]*k

                        # Check if the new position is on the board
                        if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                            # if we find a rook or queen of the opposing color, add it to checkingPieces
                            if ((self.board[rowToCheck][columnToCheck][1] == 'R') or (self.board[rowToCheck][columnToCheck][1] == 'Q')) and (self.board[rowToCheck][columnToCheck][0] == blockingColor):
                                print("block by queen or rook")
                                return True
                            elif self.board[rowToCheck][columnToCheck] == '..': # continue in the same direction if the square is empty
                                pass
                            else: # go to next direction if the square is occupied by the same color piece
                                break
                        else: # go to next direction if we go off board
                            break
                
                # check for bishops and queens 
                for direction in checkBishops:
                    for j in range(1, DIMENSION):
                        rowToCheck = rowBlock + direction[0]*j
                        columnToCheck = columnBlock + direction[1]*j
                        
                        # Check if the new position is on the board
                        if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                            # if we find a bishop or queen of the opposing color, add it to checkingPieces
                            if ((self.board[rowToCheck][columnToCheck][1] == 'B') or (self.board[rowToCheck][columnToCheck][1] == 'Q')) and (self.board[rowToCheck][columnToCheck][0] == blockingColor):
                                print("block by bishop or queen")
                                return True 
                            elif self.board[rowToCheck][columnToCheck] == '..': # continue in the same direction if the square is empty
                                pass
                            else: # go to next direction if the square is occupied by the same color piece
                                break
                        else:
                            break
                
                # check for knights 
                for direction in checkKnights:
                    rowToCheck = rowBlock + direction[0]
                    columnToCheck = columnBlock + direction[1]
                    # Check if the new position is on the board
                    if 0 <= rowToCheck < DIMENSION and 0 <= columnToCheck < DIMENSION:
                        # if we find a knight of the opposing color, add it to checkingPieces
                        if self.board[rowToCheck][columnToCheck][1] == 'N' and self.board[rowToCheck][columnToCheck][0] == blockingColor:
                            print("block by knights")
                            return True
                    
                # check for pawns that can move vertically to block check
                if blockingColor == 'w':
                    if self.board[rowBlock + 1][columnBlock] == 'wP':
                        print("blocked by white pawn")
                        return True
                    elif rowBlock + 2 == 6 and self.board[rowBlock + 2][columnBlock] == 'wP':
                        print("blocked by white pawn2")
                        return True
                else:
                    if self.board[rowBlock - 1][columnBlock] == 'bP':
                        print("blocked by black pawn at: " + str((rowBlock-1, columnBlock)))
                        return True
                    elif rowBlock - 2 == 1 and self.board[rowBlock - 2][columnBlock] == 'bP':
                        print("blocked by black pawn2")
                        return True
        
        return False

                


        




                




                                           
           
        
        
                        

        





    
