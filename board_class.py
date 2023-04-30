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

        self.board = [['..', '..', '..', '..', '..', '..', 'bK', '..'],  # Stores the location of all pieces on a 8x8 board using a 2D array 
                    ['wQ', '..', '..', '..', '..', '..', '..', '..'],    # bR denotes "black rook" and wR denotes "white rook"
                    ['..', '..', '..', '..', '..', '..', 'wP', 'wP'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', '..', '..', '..', '..'],
                    ['..', '..', '..', '..', 'wK', '..', '..', '..']]

        self.whiteTurn = True
        self.blackKingLocation = (0, 6) 
        self.whiteKingLocation = (7, 4)
        self.validMoves = [] # a list of all possible valid moves at a certain colors turn for the piece clicked on
        self.attackingPieces = [] # a list of all pieces that attack a certain square

    # generate all possible moves for a pawn 
    def allPawnMoves(self, currentRow, currentColumn, DIMENSION):

        colorOfAttackingPiece = self.getColorOfAttackingPiece()

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
                if self.checkPieceInPath(destinationRow, destinationColumn) == True and self.checkSameColor(destinationRow, destinationColumn, currentRow, currentColumn, colorOfAttackingPiece) == False:
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
        
        # keep track of what row and column the king is on 
        kingRow = currentRow 
        kingColumn = currentColumn
        king = self.board[kingRow][kingColumn]

        # print("removing the king")
        # self.board[kingRow][kingColumn] = '..'

        colorOfAttackingPiece = self.getColorOfAttackingPiece()

        moves = [(-1, -1), (-1, 1), (1, 1), (1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]

        for move in moves:
            destinationRow = currentRow + move[0]
            destinationColumn = currentColumn + move[1]
            # Check if the new position is on the board and that the new position is not attacked by other pieces
            if 0 <= destinationRow < DIMENSION and 0 <= destinationColumn < DIMENSION:
                if self.checkPieceInPath(destinationRow, destinationColumn):
                    if self.checkSameColor(destinationRow, destinationColumn, currentRow, currentColumn, colorOfAttackingPiece) == False:
                        if self.squareAttacked(destinationRow, destinationColumn, DIMENSION, colorOfAttackingPiece) == False:
                            self.validMoves.append((destinationRow, destinationColumn))
                elif self.squareAttacked(destinationRow, destinationColumn, DIMENSION, colorOfAttackingPiece) == False:
                    self.validMoves.append((destinationRow, destinationColumn))

        # print("brining king back")
        # self.board[kingRow][kingColumn] = king

    # returns the color of the attacking piece for generating all valid moves for a piece of a certain color
    def getColorOfAttackingPiece(self):
        if self.whiteTurn == False:
            
            colorOfAttackingPiece = 'w'
            print("It is black's turn so the color of attacking piece is: " + colorOfAttackingPiece)

        else:
            colorOfAttackingPiece = 'b'
            print("It is white's turn so the color of attacking piece is: " + colorOfAttackingPiece)


        return colorOfAttackingPiece
    
    def addMove(self, destinationRow, destinationColumn, currentRow, currentColumn):
        colorOfAttackingPiece = self.getColorOfAttackingPiece()
        # check if there is a piece in the way
        if self.checkPieceInPath(destinationRow, destinationColumn):
            # if there is a piece in the way, check its color
            # If it is the same, cannot go there so do not append to list. If it is different, can go there, so append list

            if self.checkSameColor(destinationRow, destinationColumn, currentRow, currentColumn, colorOfAttackingPiece) == False:
                self.validMoves.append((destinationRow, destinationColumn))
        else:
            self.validMoves.append((destinationRow, destinationColumn))

    # check if there is a piece in the way
    def checkPieceInPath(self, destinationRow, destinationColumn):
        if self.board[destinationRow][destinationColumn] != '..':
            return True
        else:
            return False

    # check if the piece in the way is the same color as the piece being moved. 
    # Also checks if the color of a piece attacking an empty square is of the opponent or not 
    def checkSameColor(self, destinationRow, destinationColumn, currentRow, currentColumn, colorOfAttackingPiece):
        #pieceToMove = self.board[currentRow][currentColumn]
        pieceToReplace = self.board[destinationRow][destinationColumn]

        # checks if the square that a piece is being moved to is the color of an attacking piece
        if pieceToReplace[0] == colorOfAttackingPiece:
            return False # if the square is occupied by a piece of the attacking piece color, the pieces are not the same color 
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

    # checks if a move made by a color results in the same color king being in check
    # checks if a move made by the opposing color results in check 
    def squareAttacked(self, r, c, DIMENSION, colorOfAttackingPiece):
        self.attackingPieces.clear()

        squareAttacked = False
        
        # need to check up, down, right, left, up left, up right, down right, down left, 
        # for knights that can check the king, just pretend king is a knight and generate all moves for it

        pathsToSquare = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (1, 1), (-1, 1), 
                       (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1)]

        rowAttacked = r
        columnAttacked = c

        print("Piece attacked is at: " + str(rowAttacked) + str(columnAttacked))

        if colorOfAttackingPiece == 'w': # if it is black's turn, we need to check all white pieces that attack a square
            print("checking for attacking white pawns")
            rowOfPawnCheck = 1 # The only way for a white pawn to attack a black piece is if it is the row "below" the it
        else: 
            print("checking for attacking black pawns") 
            rowOfPawnCheck = -1 # The only way for a black pawn to attack a white piece is if it is the row "above" the piece
 
        for path in pathsToSquare:
            for i in range(1, DIMENSION):

                if path[0] == 2 or path[1] == 2 or path[0] == -2 or path[1] == -2: # look for checking knights
                    destinationRow = rowAttacked + path[0]
                    destinationColumn = columnAttacked + path[1]
                else:
                    destinationRow = rowAttacked + path[0] * i 
                    destinationColumn = columnAttacked + path[1] * i

                # Check if the new position is on the board
                if 0 <= destinationRow < DIMENSION and 0 <= destinationColumn < DIMENSION:
                    # check if there is a piece that has line of sight to the king  
                    if self.checkPieceInPath(destinationRow, destinationColumn) == True:

                        print("Piece in path: " + self.board[destinationRow][destinationColumn] + " at " + str(destinationRow) + str(destinationColumn))

                        # check if the piece is a different color 
                        if self.checkSameColor(destinationRow, destinationColumn, rowAttacked, columnAttacked, colorOfAttackingPiece) == False:

                            print("Piece is different color")

                            pieceInWay = self.board[destinationRow][destinationColumn][1]
                            if path[0] == 0 or path[1] == 0: # check if a rook or queen has vertical or horizontal line of sight to king
                                if pieceInWay == 'R' or pieceInWay == 'Q':
                                    print("attacked by rook or Queen")
                                    self.attackingPieces.append((destinationRow, destinationColumn)) # keep track of where the attacking piece is
                                    squareAttacked = True
                                else: # if the piece in the way is not a rook or queen, move to next direction
                                    break 
                            elif path[0] == 2 or path[1] == 2 or path[0] == -2 or path[1] == -2:
                                if pieceInWay == 'N':
                                    print("attacked by knight")
                                    self.attackingPieces.append((destinationRow, destinationColumn))
                                    squareAttacked = True
                                else:
                                    break
                            else: # check if a bishop or queen or pawn has diagonal line of sight to king
                                if pieceInWay == 'B' or pieceInWay == 'Q':
                                    print("attacked by bishop or queen")
                                    self.attackingPieces.append((destinationRow, destinationColumn))
                                    squareAttacked = True
                                elif pieceInWay == 'P' and rowAttacked + rowOfPawnCheck == destinationRow: # check if a pawn of the opposite color is in the appropriate row to check the king
                                    print("attacked by pawn")
                                    self.attackingPieces.append((destinationRow, destinationColumn))
                                    squareAttacked = True
                                else: # if the piece in the way is not a bishop or queen, move to next direction
                                    break
                        else: # if the piece in the way is of the same color, move in another direction
                            break
                else:
                    break # stop from going off board in a direction

        if squareAttacked == True:
            return True
        else:
            return False
                        
    def staleMate(self, DIMENSION):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = self.board[r][c][1]
                self.generateAllValidMovesForPiece(r, c, piece, DIMENSION)
        
        if self.validMoves == []:
            return True 
        else:
            self.validMoves.clear()
            return False

    def checkMate(self, DIMENSION):
        
        print ("checking for checkmate")

        # get the color of the attacking piece of a king of a certain color 
        # if the king is black, color should be white and vice versa

        colorOfAttackingPiece = self.getColorOfAttackingPiece()

        # if it is black's turn, check if black king is in check
        if self.whiteTurn == False:
            kingRow = self.blackKingLocation[0]
            kingColumn = self.blackKingLocation[1]
        else:
            kingRow = self.whiteKingLocation[0]
            kingColumn = self.whiteKingLocation[1]

        print ("The king is at: " + str(kingRow) + str(kingColumn) + str(" and the king color is: ") + str(self.board[kingRow][kingColumn][0]))

        # check if king is in check 
        print("checking if the king is in check")
        if self.squareAttacked(kingRow, kingColumn, DIMENSION, colorOfAttackingPiece) == True:
            print("The king is attacked")
            print("the attackingPieces array is: " + str(self.attackingPieces))
            attackingPieceRow = self.attackingPieces[0][0]
            attackingPieceColumn = self.attackingPieces[0][1]
            attackingPiece = self.board[attackingPieceRow][attackingPieceColumn][1]

            # check if the king can move out of check 
            print("Checking if the king can move out of check")
            self.allKingMoves(kingRow, kingColumn, DIMENSION)
            if self.validMoves != []: # if the king can move, it is not checkmate
                print("king can move out of check") 
                return False
            elif len(self.attackingPieces) == 1: # if the king cannot move out of single check. If it is a double check and it cannot, it is checkmate. 
                # check if any piece can capture the checking piece
                # print("the attackingPieces array is: " + str(self.attackingPieces))
                # attackingPieceRow = self.attackingPieces[0][0]
                # attackingPieceColumn = self.attackingPieces[0][1]
                # attackingPiece = self.board[attackingPieceRow][attackingPieceColumn][1]

                # if the king is white, we need to check for all black pieces that attack it in the beginning
                # now, we want to check if the black piece that is checking the white king is attacked, 
                # so the color of attacking piece is now white. 
                if colorOfAttackingPiece == 'b':
                    colorToCheck = 'w'
                else:
                    colorToCheck = 'b'
                
                print("The piece attacking the king is: " + str(self.board[attackingPieceRow][attackingPieceColumn]))

                # if the attacking piece can be taken, it is not checkmate
                print("checking if the attacking piece can be taken")
                if self.squareAttacked(attackingPieceRow, attackingPieceColumn, DIMENSION, colorToCheck) == True:
                    print("the attacking piece can be taken")
                    return False
                else:
                    if attackingPiece == 'N' or attackingPiece == 'P': # if the attacking piece is a knight or pawn that cannot be taken and the king cannot move, it is checkmate
                        print("check by knight or pawn")
                        return True 
                    elif attackingPiece == 'Q' or attackingPiece == 'B': # queen and bishop check
                        print("check by queen or bishop")
                        # check which direction the attacking piece is
                        if kingRow < attackingPieceRow and kingColumn < attackingPieceColumn:
                            directionOfAttackingPiece = (1, 1)
                        elif kingRow > attackingPieceRow and kingColumn > attackingPieceColumn:
                            directionOfAttackingPiece = (-1, -1)
                        elif kingRow < attackingPieceRow and kingColumn > attackingPieceColumn:
                            directionOfAttackingPiece = (1, -1)
                        else:
                            directionOfAttackingPiece = (-1, 1)
                    else: # rook and queen check
                        print("check by rook or queen")
                        if kingColumn < attackingPieceColumn:
                            directionOfAttackingPiece = (0, 1)
                        elif kingColumn > attackingPieceColumn:
                            directionOfAttackingPiece = (0, -1)
                        elif kingRow < attackingPieceRow:
                            directionOfAttackingPiece = (1, 0)
                        else:
                            directionOfAttackingPiece = (-1, 0)
                    
                    print("The direction of the attacking piece is: " + str(directionOfAttackingPiece))
                    # check if the squares in between the attacking piece and the king can be taken 
                    # loops through the squares b/w the attacking piece and king to see if the check can be blocked
                    while (True):
                        if kingRow + directionOfAttackingPiece[0] != attackingPieceRow and kingColumn + directionOfAttackingPiece[1] != attackingPieceColumn:
                            kingRow = kingRow + directionOfAttackingPiece[0]
                            kingColumn = kingColumn + directionOfAttackingPiece[1]

                            if self.squareAttacked(kingRow, kingColumn, DIMENSION, colorToCheck) == True and self.board[self.attackingPieces[0][0]][self.attackingPieces[0][1]][1] != 'P':
                                for i in range(len(self.attackingPieces)):
                                    if self.board[self.attackingPieces[i][0]][self.attackingPieces[i][1]][1] != 'P':
                                        return False
                        else: # break the loop once the attacking piece is reached
                            break
                        
                    
                    return True
            else:
                return True
        else:
            return False

                                    
                                





                        


                




                                           
           
        
        
                        

        





    
