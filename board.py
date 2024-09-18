import pygame
from piece import Piece

class Board:
    def __init__(self, size, initialize=True):
        self.rows = size
        self.cols = size
        self.window_size = 800  # Fixed window size
        self.offset = 50  # Offset for labels
        self.grid_size = (self.window_size - self.offset * 2) // size  # Dynamically calculate grid size based on board size
        self.pieces = []  # List to hold the pieces

        if initialize:  # Only initialize pieces if the flag is True
            self.initialize_pieces(size)


    def initialize_pieces(self, size):
        """Initialize pieces based on the number of players and board size."""
        if size == 8:
            self.initialize_2_player_pieces()
        else:
            self.initialize_4_player_pieces(size)

    def initialize_2_player_pieces(self):
        for i in range(1, 7):
            self.pieces.append(Piece(0, i, (0, 0, 0)))  # Top row (black)
            self.pieces.append(Piece(7, i, (0, 0, 0)))  # Bottom row (black)
        for i in range(1, 7):
            self.pieces.append(Piece(i, 0, (255, 255, 255)))  # Left column (white)
            self.pieces.append(Piece(i, 7, (255, 255, 255)))  # Right column (white)

    def initialize_4_player_pieces(self, size):
        empty_spaces = (size - 6) // 2
        for i in range(6):
            col_position = empty_spaces + i
            color = (0, 0, 0) if i % 2 == 0 else (255, 0, 0)  # Black (B) and Red (R)
            self.pieces.append(Piece(0, col_position, color))  # Top row
            self.pieces.append(Piece(size - 1, col_position, color))  # Bottom row
        for i in range(6):
            row_position = empty_spaces + i
            color = (255, 255, 255) if i % 2 == 0 else (0, 255, 0)  # White (W) and Green (G)
            self.pieces.append(Piece(row_position, 0, color))  # Left column
            self.pieces.append(Piece(row_position, size - 1, color))  # Right column

    def draw(self, window, selected_piece=None):
        tan_color = (210, 180, 140)
        font = pygame.font.SysFont('Arial', 24)
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * self.grid_size + self.offset, row * self.grid_size + self.offset, self.grid_size, self.grid_size)
                pygame.draw.rect(window, tan_color, rect)
                pygame.draw.rect(window, (0, 0, 0), rect, 1)
                piece = self.get_piece(row, col)
                if piece:
                    if piece == selected_piece:
                        self.outline_piece(window, piece)
                    piece.draw(window, self.grid_size, self.offset)
        for col in range(self.cols):
            label = font.render(chr(65 + col), True, (0, 0, 0))
            label_rect = label.get_rect(center=(col * self.grid_size + self.offset + self.grid_size // 2, self.rows * self.grid_size + self.offset + 20))
            window.blit(label, label_rect)
        for row in range(self.rows):
            label = font.render(str(self.rows - row), True, (0, 0, 0))
            label_rect = label.get_rect(center=(self.offset - 20, row * self.grid_size + self.offset + self.grid_size // 2))
            window.blit(label, label_rect)

    def outline_piece(self, window, piece):
        outline_color = (255, 215, 0)
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
            if piece:
                if piece.color != color:
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

    def get_remaining_colors(self):
        """Returns a set of remaining colors on the board."""
        remaining_colors = set()
        for piece in self.pieces:
            remaining_colors.add(piece.color)
        return remaining_colors

    def get_remaining_colors(self):
        """Returns a set of remaining colors on the board."""
        remaining_colors = set()
        for piece in self.pieces:
            remaining_colors.add(piece.color)
        return remaining_colors

    def check_connected_group(self, color):
        """Check if all pieces of a specified color are connected, or if only one color remains on the board."""
        #print(f"Color is: {color}")
        # Debugging: Display current pieces on the board
        print(f"Checking connected group for color: {self.get_color_name(color)}")
        #print(f"Current pieces on the board: {[f'({piece.row}, {piece.col}, {self.get_color_name(piece.color)})' for piece in self.pieces]}")

        # Check if only one color remains on the board
        remaining_colors = self.get_remaining_colors()
        #print(f"Remaining colors on board: {[self.get_color_name(c) for c in remaining_colors]}")  # Debugging statement

        if len(remaining_colors) == 1:
            print("Only one color remains on the board, automatic winner.")
            return True

        # Proceed with the regular check for connected groups
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
            print("No starting piece found for this color.")
            return False

        #print(f"Starting DFS from piece at ({start_row}, {start_col}) for color {self.get_color_name(color)}")  # Debugging

        # Start DFS from the first found piece
        self.dfs(start_row, start_col, color, visited)

        # Check if all pieces of the color are visited
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color and not visited[row][col]:
                    return False

        print(f"All pieces of color {self.get_color_name(color)} are connected.")
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

    def get_color_name(self, color):
        """Convert an RGB color tuple to a string representing the color name."""
        if color == (0, 0, 0):
            return "Black"
        elif color == (255, 255, 255):
            return "White"
        elif color == (255, 0, 0):
            return "Red"
        elif color == (0, 255, 0):
            return "Green"
        else:
            return "Unknown"

    def clear_board(self):
        """Clears all pieces from the board."""
        self.pieces.clear()  # Clears all elements in the pieces list

    def set_piece(self, row, col, color):
        """Places a piece at the specified position on the board."""
        #print(f"Setting piece at ({row}, {col}) with color {color}")  # Debugging statement
        self.pieces.append(Piece(row, col, color))  # Add piece to the list
        #print(f"Current pieces on board: {[f'({p.row}, {p.col}, {p.color})' for p in self.pieces]}")  # Debugging statement
