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
        if bs.checkValidTurn(clicks) == True:
            print("It is your turn")
            if bs.checkMate(DIMENSION) == False:
                print("The king is not in check")
                bs.validMoves.clear()
                if bs.checkValidMove(clicks, DIMENSION) == True:
                    print("that is a valid move")
                    temp = bs.board[clicks[0]][clicks[1]]
                    bs.board[clicks[0]][clicks[1]] = '..'
                    pieceEaten = bs.board[clicks[2]][clicks[3]]
                    bs.board[clicks[2]][clicks[3]] = temp

                    # keep track of both king locations
                    if temp == 'bK':
                        bs.blackKingLocation = (r, c)
                    elif temp == 'wK':
                        bs.whiteKingLocation = (r, c)
                    
                    # if it is blacks or whites turn, check if the move results in black/white king in check 
                    if (bs.whiteTurn == False and bs.squareAttacked(bs.blackKingLocation[0], bs.blackKingLocation[1], DIMENSION) == False) or (bs.whiteTurn == True and bs.squareAttacked(bs.whiteKingLocation[0], bs.whiteKingLocation[1], DIMENSION) == False):
                        bs.whiteTurn = not bs.whiteTurn 

                        

                        # if bs.staleMate(DIMENSION) == True: 
                        #     print("Stalemate")

                            
                    else: 
                        temp = bs.board[clicks[2]][clicks[3]]
                        bs.board[clicks[2]][clicks[3]] = pieceEaten
                        bs.board[clicks[0]][clicks[1]] = temp 
                        
                        # move the king location back to the original location if the move is invalid for the king
                        if temp == 'bK':
                            bs.blackKingLocation = (clicks[0], clicks[1])
                        elif temp == 'wK':
                            bs.whiteKingLocation = (clicks[0], clicks[1])
            else:
                print("CheckMate")

        clicks.clear()

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


