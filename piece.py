# piece.py

import pygame

class Piece:
    """
    Function Name: __init__
    Purpose: To initialize a piece with its position and color.
    Parameters:
        row (int), the row where the piece is placed.
        col (int), the column where the piece is placed.
        color (tuple), the RGB color of the piece.
    Return Value: None
    Algorithm:
        1) Assign the row, column, and color to the piece.
    Reference: None
    """
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    """
    Function Name: draw
    Purpose: To draw a piece on the game window.
    Parameters:
        window (pygame.Surface), the window where the piece will be drawn.
        grid_size (int), the size of each grid square on the board.
        offset (int), optional parameter to adjust the position (default is 0).
    Return Value: None
    Algorithm:
        1) Calculate the radius and center of the piece.
        2) Draw the piece as a circle on the game window using its color and position.
    Reference: None
    """
    def draw(self, window, grid_size, offset=0):
        radius = grid_size // 2 - 10
        center = (self.col * grid_size + grid_size // 2 + offset, self.row * grid_size + grid_size // 2 + offset)
        pygame.draw.circle(window, self.color, center, radius)
