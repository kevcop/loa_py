import pygame
from piece import Piece

class Board:
    def __init__(self, size):
        self.size = size
        self.rows = self.size  # Set number of rows based on size
        self.cols = self.size  # Set number of columns based on size
        self.window_size = 800  # Default window size for 8x8

        # Dynamically adjust grid size based on board size
        if self.size == 8:
            self.grid_size = 80  # 8x8
        elif self.size == 12:
            self.grid_size = 50  # 12x12
        elif self.size == 16:
            self.grid_size = 40  # 16x16

        self.offset = 50  # Offset for labels
        self.pieces = []
        self.initialize_pieces()

    def initialize_pieces(self):
        piece_count = 6  # We are using 6 pieces for all board sizes

        if self.size == 8:
            # Place 6 pieces with 1 empty space at both ends
            for i in range(1, 7):  # 6 pieces in the middle (1 empty space on each end)
                self.pieces.append(Piece(0, i, (0, 0, 0)))  # Top row (black)
                self.pieces.append(Piece(7, i, (0, 0, 0)))  # Bottom row (black)
            for i in range(1, 7):
                self.pieces.append(Piece(i, 0, (255, 255, 255)))  # Left column (white)
                self.pieces.append(Piece(i, 7, (255, 255, 255)))  # Right column (white)

        elif self.size == 12:
            # Place 6 pieces with 3 empty spaces on each end
            for i in range(3, 9):  # 6 pieces in the middle (3 empty spaces on each end)
                self.pieces.append(Piece(0, i, (0, 0, 0)))  # Top row (black)
                self.pieces.append(Piece(11, i, (0, 0, 0)))  # Bottom row (black)
            for i in range(3, 9):
                self.pieces.append(Piece(i, 0, (255, 255, 255)))  # Left column (white)
                self.pieces.append(Piece(i, 11, (255, 255, 255)))  # Right column (white)

        elif self.size == 16:
            # Place 6 pieces with 5 empty spaces on each end
            for i in range(5, 11):  # 6 pieces in the middle (5 empty spaces on each end)
                self.pieces.append(Piece(0, i, (0, 0, 0)))  # Top row (black)
                self.pieces.append(Piece(15, i, (0, 0, 0)))  # Bottom row (black)
            for i in range(5, 11):
                self.pieces.append(Piece(i, 0, (255, 255, 255)))  # Left column (white)
                self.pieces.append(Piece(i, 15, (255, 255, 255)))  # Right column (white)

    def draw(self, window, selected_piece=None):
        tan_color = (210, 180, 140)
        font = pygame.font.SysFont('Arial', 24)

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
        target_piece = self.get_piece(row, col)
        if target_piece and target_piece.color != piece.color:
            self.remove_piece(target_piece)

        piece.row = row
        piece.col = col

    def is_valid_move(self, piece, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False, "Move is out of bounds."

        if self.get_piece(row, col) and self.get_piece(row, col).color == piece.color:
            return False, "Cannot move to a square occupied by your own piece."

        if piece.row == row:
            distance = abs(col - piece.col)
            line_pieces = self.count_pieces_on_line(piece.row, is_row=True)
            if not self.is_path_clear(piece.row, piece.col, row, col, piece.color):
                return False, "Path is blocked by an opponent's piece."
        elif piece.col == col:
            distance = abs(row - piece.row)
            line_pieces = self.count_pieces_on_line(piece.col, is_row=False)
            if not self.is_path_clear(piece.row, piece.col, row, col, piece.color):
                return False, "Path is blocked by an opponent's piece."
        elif abs(piece.row - row) == abs(piece.col - col):
            distance = abs(row - piece.row)
            line_pieces = self.count_diagonal_pieces(piece.row, piece.col, row, col)
            if not self.is_path_clear(piece.row, piece.col, row, col, piece.color):
                return False, "Path is blocked by an opponent's piece."
        else:
            return False, "Invalid move: Not a straight line or diagonal."

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
            if piece and piece.color != color:
                return False
            current_row += d_row
            current_col += d_col

        return True

    def count_diagonal_pieces(self, start_row, start_col, end_row, end_col):
        count = 0

        d_row = 1 if end_row > start_row else -1
        d_col = 1 if end_col > start_col else -1

        row, col = start_row, start_col
        while row >= 0 and row < self.rows and col >= 0 and col < self.cols:
            if self.get_piece(row, col):
                count += 1
            row -= d_row
            col -= d_col

        row, col = start_row + d_row, start_col + d_col
        while row >= 0 and row < self.rows and col >= 0 and col < self.cols:
            if self.get_piece(row, col):
                count += 1
            row += d_row
            col += d_col

        return count

    def count_pieces_on_line(self, index, is_row=True):
        count = 0

        if is_row:
            for col in range(self.cols):
                if self.get_piece(index, col):
                    count += 1
        else:
            for row in range(self.rows):
                if self.get_piece(row, index):
                    count += 1

        return count

    def get_position_notation(self, row, col):
        column_label = chr(65 + col)
        row_label = str(self.rows - row)
        return f"{column_label}{row_label}"

    def check_connected_group(self, color):
        start_row, start_col = -1, -1
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    start_row, start_col = row, col
                    break
            if start_row != -1:
                break

        if start_row == -1:
            return False

        self.dfs(start_row, start_col, color, visited)

        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color and not visited[row][col]:
                    return False

        return True

    def dfs(self, row, col, color, visited):
        row_nbr = [-1, 1, 0, 0, -1, -1, 1, 1]
        col_nbr = [0, 0, -1, 1, -1, 1, -1, 1]

        visited[row][col] = True

        for k in range(8):
            new_row = row + row_nbr[k]
            new_col = col + col_nbr[k]
            if self.is_safe(new_row, new_col, color, visited):
                self.dfs(new_row, new_col, color, visited)

    def is_safe(self, row, col, color, visited):
        return (0 <= row < self.rows) and (0 <= col < self.cols) and \
               self.get_piece(row, col) and self.get_piece(row, col).color == color and \
               not visited[row][col]
