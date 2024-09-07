# board.py

import pygame
from piece import Piece

class Board:
    def __init__(self):
        self.rows = 8
        self.cols = 8
        self.grid_size = 80  # Grid size
        self.offset = 50  # Offset for labels
        self.pieces = []  # List to hold the pieces

        self.initialize_pieces()

    def initialize_pieces(self):
        # Placing black pieces on the top and bottom rows, excluding corners
        for i in range(1, 7):  # Skip the first and last columns for the top and bottom rows
            self.pieces.append(Piece(0, i, (0, 0, 0)))  # Top row
            self.pieces.append(Piece(7, i, (0, 0, 0)))  # Bottom row

        # Placing white pieces on the left and right columns, excluding corners
        for i in range(1, 7):  # Skip the first and last rows for the left and right columns
            self.pieces.append(Piece(i, 0, (255, 255, 255)))  # Left column
            self.pieces.append(Piece(i, 7, (255, 255, 255)))  # Right column

    def draw(self, window, selected_piece=None):
        # Draw the board with tan background
        tan_color = (210, 180, 140)
        font = pygame.font.SysFont('Arial', 24)

        # Draw the grid and pieces
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * self.grid_size + self.offset, row * self.grid_size + self.offset, self.grid_size, self.grid_size)
                pygame.draw.rect(window, tan_color, rect)
                pygame.draw.rect(window, (0, 0, 0), rect, 1)  # Grid lines

                # Draw the pieces and outline the selected piece
                piece = self.get_piece(row, col)
                if piece:
                    if piece == selected_piece:
                        self.outline_piece(window, piece)
                    piece.draw(window, self.grid_size, self.offset)

        # Draw the column headings (A-H) below the grid
        for col in range(self.cols):
            label = font.render(chr(65 + col), True, (0, 0, 0))
            label_rect = label.get_rect(center=(col * self.grid_size + self.offset + self.grid_size // 2, self.rows * self.grid_size + self.offset + 20))
            window.blit(label, label_rect)

        # Draw the row headings (1-8) to the left of the grid
        for row in range(self.rows):
            label = font.render(str(self.rows - row), True, (0, 0, 0))
            label_rect = label.get_rect(center=(self.offset - 20, row * self.grid_size + self.offset + self.grid_size // 2))
            window.blit(label, label_rect)

    def outline_piece(self, window, piece):
        outline_color = (255, 215, 0)  # Gold color for outlining
        outline_rect = pygame.Rect(piece.col * self.grid_size + self.offset, piece.row * self.grid_size + self.offset, self.grid_size, self.grid_size)
        pygame.draw.rect(window, outline_color, outline_rect, 5)

    def get_piece(self, row, col):
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return piece
        return None

    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def move_piece(self, piece, row, col):
        # Check if there's an opponent piece at the destination
        target_piece = self.get_piece(row, col)
        if target_piece and target_piece.color != piece.color:
            self.remove_piece(target_piece)  # Capture the opponent's piece

        # Move the piece to the new position
        piece.row = row
        piece.col = col

    def is_valid_move(self, piece, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False, "Move is out of bounds."

        if self.get_piece(row, col) and self.get_piece(row, col).color == piece.color:
            return False, "Cannot move to a square occupied by your own piece."

        # Determine the type of move
        if piece.row == row:
            # Horizontal move
            distance = abs(col - piece.col)
            line_pieces = self.count_pieces_on_line(piece.row, is_row=True)
            if not self.is_path_clear(piece.row, piece.col, row, col, piece.color):
                return False, "Path is blocked by an opponent's piece."
        elif piece.col == col:
            # Vertical move
            distance = abs(row - piece.row)
            line_pieces = self.count_pieces_on_line(piece.col, is_row=False)
            if not self.is_path_clear(piece.row, piece.col, row, col, piece.color):
                return False, "Path is blocked by an opponent's piece."
        elif abs(piece.row - row) == abs(piece.col - col):
            # Diagonal move
            distance = abs(row - piece.row)
            line_pieces = self.count_diagonal_pieces(piece.row, piece.col, row, col)
            if not self.is_path_clear(piece.row, piece.col, row, col, piece.color):
                return False, "Path is blocked by an opponent's piece."
        else:
            return False, "Invalid move: Not a straight line or diagonal."

        # Validate the move distance against the number of pieces on the line
        if distance != line_pieces:
            return False, f"Invalid move distance: Attempted {distance}, but required {line_pieces}."

        return True, ""

    def is_path_clear(self, start_row, start_col, end_row, end_col, color):
        d_row = (end_row - start_row) // max(1, abs(end_row - start_row))
        d_col = (end_col - start_col) // max(1, abs(end_col - start_col))

        current_row = start_row + d_row
        current_col = start_col + d_col

        while current_row != end_row or current_col != end_col:
            piece = self.get_piece(current_row, current_col)
            if piece:
                if piece.color != color:
                    return False  # Path is blocked by an opponent's piece
            current_row += d_row
            current_col += d_col

        return True

    def count_diagonal_pieces(self, start_row, start_col, end_row, end_col):
        count = 0

        # Calculate the directions for row and column
        d_row = 1 if end_row > start_row else -1
        d_col = 1 if end_col > start_col else -1

        # Count pieces along the entire diagonal
        row, col = start_row, start_col
        while row >= 0 and row < self.rows and col >= 0 and col < self.cols:
            if self.get_piece(row, col):
                count += 1
            row -= d_row
            col -= d_col

        row, col = start_row + d_row, start_col + d_col  # Start after the initial piece
        while row >= 0 and row < self.rows and col >= 0 and col < self.cols:
            if self.get_piece(row, col):
                count += 1
            row += d_row
            col += d_col

        return count

    def count_pieces_on_line(self, index, is_row=True):
        count = 0

        if is_row:
            # Count pieces in the row (index is the row number)
            for col in range(self.cols):
                if self.get_piece(index, col):
                    count += 1
        else:
            # Count pieces in the column (index is the column number)
            for row in range(self.rows):
                if self.get_piece(row, index):
                    count += 1

        return count

    def get_position_notation(self, row, col):
        column_label = chr(65 + col)  # Convert column index to letter
        row_label = str(self.rows - row)  # Convert row index to 1-8
        return f"{column_label}{row_label}"

    def check_connected_group(self, color):
        start_row, start_col = -1, -1
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        # Find the starting piece of the given color
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    start_row, start_col = row, col
                    break
            if start_row != -1:
                break

        # If no starting piece was found, return False
        if start_row == -1:
            return False

        # Start DFS from the first found piece
        self.dfs(start_row, start_col, color, visited)

        # Check if all pieces of the color are visited
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color and not visited[row][col]:
                    return False

        return True

    def dfs(self, row, col, color, visited):
        # Define search directions (N, S, E, W, NE, NW, SE, SW)
        row_nbr = [-1, 1, 0, 0, -1, -1, 1, 1]
        col_nbr = [0, 0, -1, 1, -1, 1, -1, 1]

        # Mark this cell as visited
        visited[row][col] = True

        # Recur for all connected neighbors
        for k in range(8):
            new_row = row + row_nbr[k]
            new_col = col + col_nbr[k]
            if self.is_safe(new_row, new_col, color, visited):
                self.dfs(new_row, new_col, color, visited)

    def is_safe(self, row, col, color, visited):
        # Check if the cell is within bounds, matches the color, and has not been visited
        return (0 <= row < self.rows) and (0 <= col < self.cols) and \
               self.get_piece(row, col) and self.get_piece(row, col).color == color and \
               not visited[row][col]
