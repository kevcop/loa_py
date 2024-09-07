# piece.py

import pygame

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def draw(self, window, grid_size, offset=0):
        radius = grid_size // 2 - 10
        center = (self.col * grid_size + grid_size // 2 + offset, self.row * grid_size + grid_size // 2 + offset)
        pygame.draw.circle(window, self.color, center, radius)
