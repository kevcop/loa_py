import random
from board import Board

# Mapping of index to column notation (A-H)
index_to_col = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D',
    4: 'E', 5: 'F', 6: 'G', 7: 'H'
}

class ComputerPlayer:
    def __init__(self, board, color=(255, 255, 255)):  # Add color as an argument with default white
        self.board = board
        self.color = color  # Use the passed color
        self.possible_moves = []

    # Update the column mapping to handle more columns, supporting up to 16 columns
    def proper_notation(self, position):
        col, row = position
        column_letter = chr(65 + col)  # Convert column index to A, B, C, etc., dynamically for larger boards
        row_number = row + 1  # Adjust for 1-based row index
        return f"{column_letter}{row_number}"

    def generate_all_possible_moves(self):
        self.possible_moves.clear()
        print(f"Generating moves for color: {self.color}")

        # Iterate through all pieces on the board
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.get_piece(row, col)

                if piece:  # Only proceed if a piece exists
                    print(f"Found piece at {self.proper_notation((col, row))} with color {piece.color}")

                    # Check if the piece matches the AI's color
                    print(f"piece color is {piece.color}")
                    print(f"self color is {self.color}")
                    if piece.color == self.color:
                        self.generate_moves_for_piece(row, col)
                else:
                    print(f"No piece at {self.proper_notation((col, row))}")

        print(f"Total possible moves generated: {len(self.possible_moves)}")

    def generate_moves_for_piece(self, start_row, start_col):
        # Horizontal moves
        horizontal_moves_required = self.board.count_pieces_on_line(start_row, is_row=True)
        print(f"Horizontal moves required for piece at {self.proper_notation((start_col, start_row))}: {horizontal_moves_required}")

        for offset in range(1, horizontal_moves_required + 1):
            self.add_move_if_valid(start_row, start_col, start_row, start_col + offset)  # Right
            self.add_move_if_valid(start_row, start_col, start_row, start_col - offset)  # Left

        # Vertical moves
        vertical_moves_required = self.board.count_pieces_on_line(start_col, is_row=False)
        print(f"Vertical moves required for piece at {self.proper_notation((start_col, start_row))}: {vertical_moves_required}")

        for offset in range(1, vertical_moves_required + 1):
            self.add_move_if_valid(start_row, start_col, start_row + offset, start_col)  # Down
            self.add_move_if_valid(start_row, start_col, start_row - offset, start_col)  # Up

        # Diagonal moves
        diagonal_moves_required = self.board.count_diagonal_pieces(start_row, start_col, start_row, start_col)
        print(f"Diagonal moves required for piece at {self.proper_notation((start_col, start_row))}: {diagonal_moves_required}")

        for offset in range(1, diagonal_moves_required + 1):
            self.add_move_if_valid(start_row, start_col, start_row + offset, start_col + offset)  # Bottom-right
            self.add_move_if_valid(start_row, start_col, start_row - offset, start_col - offset)  # Top-left
            self.add_move_if_valid(start_row, start_col, start_row + offset, start_col - offset)  # Bottom-left
            self.add_move_if_valid(start_row, start_col, start_row - offset, start_col + offset)  # Top-right

    def add_move_if_valid(self, start_row, start_col, end_row, end_col):
        if 0 <= end_row < self.board.rows and 0 <= end_col < self.board.cols:
            print(f"Checking move from {self.proper_notation((start_col, start_row))} to {self.proper_notation((end_col, end_row))}")
            is_valid, captures = self.validate_move(start_row, start_col, end_row, end_col)
            if is_valid:
                print(f"Valid move from {self.proper_notation((start_col, start_row))} to {self.proper_notation((end_col, end_row))} with captures: {captures}")
                move_details = {
                    'start': (start_row, start_col),
                    'end': (end_row, end_col),
                    'captures': captures
                }
                self.possible_moves.append(move_details)
            else:
                print(f"Invalid move from {self.proper_notation((start_col, start_row))} to {self.proper_notation((end_col, end_row))}")

    def validate_move(self, start_row, start_col, end_row, end_col):
        captures = []
        piece = self.board.get_piece(start_row, start_col)
        if not piece or piece.color != self.color:  # Only validate for pieces controlled by AI
            print(f"No valid piece at start {self.proper_notation((start_col, start_row))}")
            return False, captures

        is_valid, message = self.board.is_valid_move(piece, end_row, end_col)
        if is_valid:
            target_piece = self.board.get_piece(end_row, end_col)
            if target_piece and target_piece.color != self.color:
                captures.append((end_row, end_col))
            return True, captures

        print(f"Move from {self.proper_notation((start_col, start_row))} to {self.proper_notation((end_col, end_row))} is invalid: {message}")
        return False, captures

    def select_and_execute_move(self):
        if not self.possible_moves:
            print("No possible moves to select from.")
            return

        # Randomly select a move
        selected_move = random.choice(self.possible_moves)

        start = selected_move['start']
        end = selected_move['end']

        start_notation = self.proper_notation((start[1], start[0]))  # Converting row, col to notation
        end_notation = self.proper_notation((end[1], end[0]))

        # Attempt to execute the move
        piece = self.board.get_piece(start[0], start[1])
        if piece and self.board.is_valid_move(piece, end[0], end[1])[0]:
            self.board.move_piece(piece, end[0], end[1])
            print(f"AI moved from {start_notation} to {end_notation}")

            # Process potential captures
            if selected_move['captures']:
                for capture in selected_move['captures']:
                    captured_piece = self.board.get_piece(capture[0], capture[1])
                    if captured_piece:
                        self.board.remove_piece(captured_piece)
                        print(f"Captured piece at {self.proper_notation((capture[1], capture[0]))}")
        else:
            print(f"Failed to execute move: {start_notation} to {end_notation}")

    def make_move(self):
        self.generate_all_possible_moves()
        self.select_and_execute_move()
