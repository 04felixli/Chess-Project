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
        if checkValidMove(bs) == True:
            temp = bs.board[clicks[0]][clicks[1]]
            bs.board[clicks[0]][clicks[1]] = '..'
            bs.board[clicks[2]][clicks[3]] = temp

            # keep track of both king locations
            if temp == 'bK':
                bs.blackKingLocation = (r, c)
            elif temp == 'wK':
                bs.whiteKingLocation = (r, c)

        clicks.clear()

def checkValidMove(bs):
    pieceClickedOn = bs.board[clicks[0]][clicks[1]][1]
    destination = (clicks[2], clicks[3])
    if pieceClickedOn == 'P':
        bs.allPawnMoves(clicks, DIMENSION)
    elif pieceClickedOn == 'N':
        bs.allKnightMoves(clicks, DIMENSION)
    elif pieceClickedOn == 'B':
        bs.allBishopMoves(clicks, DIMENSION)
    elif pieceClickedOn == 'R':
        bs.allRookMoves(clicks, DIMENSION)
    elif pieceClickedOn == 'Q':
        bs.allRookMoves(clicks, DIMENSION)
        bs.allBishopMoves(clicks, DIMENSION)
    elif pieceClickedOn == 'K':
        bs.allKingMoves(clicks, DIMENSION)
    
    if destination in bs.validMoves:
        bs.validMoves.clear()
        return True
    else:
        return False
    
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


