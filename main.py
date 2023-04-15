# This file is responsible for running the actual game
import pygame 
import os
from board_class import Board

WIDTH = HEIGHT = 512 # size of window 
DIMENSION = 8 # board is made of 8x8 squares 

SQUARE_SIZE = WIDTH // DIMENSION
FPS = 10

IMAGES = {}

clicks = [] # (row of click 1, column of click 1, row of click 2, column of click 2)

# Create a hashmap of images that maps "piece_name : image"

def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(os.path.join('images', piece + '.png')), (SQUARE_SIZE, SQUARE_SIZE))

def drawBoard(bs, window):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # print board
            color = colors[((r+c) % 2)]
            rect = pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # create rectangle at (x_location, y_location, x_dim, y_dim)
            pygame.draw.rect(window, color, rect)

            # print pieces on board
            if bs.board[r][c] != '..':
                window.blit(IMAGES[bs.board[r][c]], (c*SQUARE_SIZE, r*SQUARE_SIZE))

def movePiece(bs):
    mouseClickLocation = pygame.mouse.get_pos() # gets the (x,y) of mouse click
    r = mouseClickLocation[1] // SQUARE_SIZE # returns the row of the box clicked on
    c = mouseClickLocation[0] // SQUARE_SIZE # returns the column of the box clicked on

    clicks.append(r)
    clicks.append(c)

    if len(clicks) == 4: # on second click the player moves the peice from a to b
        if checkValidTurn(bs) == True:
            print("It is your turn")
            if checkValidMove(bs) == True:
                print("that is a valid move")
                temp = bs.board[clicks[0]][clicks[1]]
                bs.board[clicks[0]][clicks[1]] = '..'
                bs.board[clicks[2]][clicks[3]] = temp

                # # keep track of both king locations
                # if temp == 'bK':
                #     bs.blackKingLocation = (r, c)
                # elif temp == 'wK':
                #     bs.whiteKingLocation = (r, c)

                # bs.whiteTurn = not bs.whiteTurn
                                
                if checkCheck(bs) == False:
                    # keep track of both king locations
                    if temp == 'bK':
                        bs.blackKingLocation = (r, c)
                    elif temp == 'wK':
                        bs.whiteKingLocation = (r, c)

                    bs.whiteTurn = not bs.whiteTurn
                else: 
                    temp = bs.board[clicks[2]][clicks[3]]
                    bs.board[clicks[2]][clicks[3]] = '..'
                    bs.board[clicks[0]][clicks[1]] = temp

        clicks.clear()

# checks if a piece can move to a certain location
def checkValidMove(bs):
    pieceClickedOn = bs.board[clicks[0]][clicks[1]][1]
    destination = (clicks[2], clicks[3])
    generateAllValidMovesForPiece(bs, clicks[0], clicks[1], pieceClickedOn)
    # if pieceClickedOn == 'P':
    #     bs.allPawnMoves(clicks, DIMENSION)
    # elif pieceClickedOn == 'N':
    #     bs.allKnightMoves(clicks, DIMENSION)
    # elif pieceClickedOn == 'B':
    #     bs.allBishopMoves(clicks, DIMENSION)
    # elif pieceClickedOn == 'R':
    #     bs.allRookMoves(clicks, DIMENSION)
    # elif pieceClickedOn == 'Q':
    #     bs.allRookMoves(clicks, DIMENSION)
    #     bs.allBishopMoves(clicks, DIMENSION)
    # elif pieceClickedOn == 'K':
    #     bs.allKingMoves(clicks, DIMENSION)
    
    if destination in bs.validMoves:
        bs.validMoves.clear()
        return True
    else:
        return False
    
# checks who's turn it is
def checkValidTurn(bs):
    currentRow = clicks[0] # row the piece is on before being moved
    currentColumn = clicks[1] # column the piece is on before being moved
    destinationRow = clicks[2]
    destinationColumn = clicks[3]
    pieceToMove = bs.board[currentRow][currentColumn]
    destination = bs.board[destinationRow][destinationColumn] 
    pieceMovedColor = pieceToMove[0]
    destinationColor = destination[0]

    # returns true if the piece being moved is the correct color, false otherwise
    if ((pieceMovedColor == 'w' != destinationColor) and bs.whiteTurn == True) or ((pieceMovedColor == 'b' != destinationColor) and bs.whiteTurn == False):
        return True
    else:
        return False

# check if a move results in a king being in check. Returns True is yes, False, if no
def checkCheck(bs):

    # check all piece of colors opposite to the color of the piece that just moved
    if bs.whiteTurn == False:
        colorToCheck = 'w'
        print("Black made a turn, the color to check is white")
    else:
        colorToCheck = 'b'
        print("White made a turn, the color to check is black")

    generateAllResponseMoves(bs, colorToCheck)

    # check if any piece of the opposite color can move to opposite kings location after the opposite color moves a piece
    # if a piece can, that move is invalid so return True, else return False since move is valid. 
    if ((bs.whiteTurn == False) and (bs.blackKingLocation in bs.validMoves)) or ((bs.whiteTurn == True) and (bs.whiteKingLocation in bs.validMoves)):
        return True
    else: 
        bs.validMoves.clear()
        return False



# generates all possible moves for a color in response to the other color moving a piece
def generateAllResponseMoves(bs, colorToCheck):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pieceColor = bs.board[r][c][0]
            piece = bs.board[r][c][1]
            if pieceColor == colorToCheck:
                print("The color of the piece I am checking is: " + str(pieceColor))
                print("The piece I am checking is: " + str(piece))
                generateAllValidMovesForPiece(bs, r, c, piece)
                print("The moves I can make are: " + str(bs.validMoves))

# generates all valid moves for a piece at it's currentRow and currentColumn
def generateAllValidMovesForPiece(bs, currentRow, currentColumn, piece):
    if piece == 'P':
        bs.allPawnMoves(currentRow, currentColumn, DIMENSION)
    elif piece == 'N':
        bs.allKnightMoves(currentRow, currentColumn, DIMENSION)
    elif piece == 'B':
        bs.allBishopMoves(currentRow, currentColumn, DIMENSION)
    elif piece == 'R':
        # bs.allRookMoves(clicks, DIMENSION)
        bs.allRookMoves(currentRow, currentColumn, DIMENSION)
    elif piece == 'Q':
        bs.allRookMoves(currentRow, currentColumn, DIMENSION)
        bs.allBishopMoves(currentRow, currentColumn, DIMENSION)
    elif piece == 'K':
        bs.allKingMoves(currentRow, currentColumn, DIMENSION)



def main():
    pygame.init()
    run = True
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    window.fill(pygame.Color("white"))
    bs = Board() # create game board
    loadImages() # only load images once

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                movePiece(bs)

        drawBoard(bs, window)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()


