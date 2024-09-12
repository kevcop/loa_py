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
        self.capture_moves = []  # Store capture moves separately

    # Update the column mapping to handle more columns, supporting up to 16 columns
    def proper_notation(self, position):
        col, row = position
        column_letter = chr(65 + col)  # Convert column index to A, B, C, etc., dynamically for larger boards
        row_number = row + 1  # Adjust for 1-based row index
        return f"{column_letter}{row_number}"

    def generate_all_possible_moves(self):
        self.possible_moves.clear()
        self.capture_moves.clear()  # Clear the capture moves list
        #print(f"Generating moves for color: {self.color}")

        # Iterate through all pieces on the board
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.get_piece(row, col)

                if piece:  # Only proceed if a piece exists
                    #print(f"Found piece at {self.proper_notation((col, row))} with color {piece.color}")

                    # Check if the piece matches the AI's color
                    if piece.color == self.color:
                        self.generate_moves_for_piece(row, col)

        #print(f"Total possible moves generated: {len(self.possible_moves)}")
        #print(f"Total capture moves generated: {len(self.capture_moves)}")

    def generate_moves_for_piece(self, start_row, start_col):
        # Horizontal moves
        horizontal_moves_required = self.board.count_pieces_on_line(start_row, is_row=True)
        for offset in range(1, horizontal_moves_required + 1):
            self.add_move_if_valid(start_row, start_col, start_row, start_col + offset)  # Right
            self.add_move_if_valid(start_row, start_col, start_row, start_col - offset)  # Left

        # Vertical moves
        vertical_moves_required = self.board.count_pieces_on_line(start_col, is_row=False)
        for offset in range(1, vertical_moves_required + 1):
            self.add_move_if_valid(start_row, start_col, start_row + offset, start_col)  # Down
            self.add_move_if_valid(start_row, start_col, start_row - offset, start_col)  # Up

        # Diagonal moves
        diagonal_moves_required = self.board.count_diagonal_pieces(start_row, start_col, start_row, start_col)
        for offset in range(1, diagonal_moves_required + 1):
            self.add_move_if_valid(start_row, start_col, start_row + offset, start_col + offset)  # Bottom-right
            self.add_move_if_valid(start_row, start_col, start_row - offset, start_col - offset)  # Top-left
            self.add_move_if_valid(start_row, start_col, start_row + offset, start_col - offset)  # Bottom-left
            self.add_move_if_valid(start_row, start_col, start_row - offset, start_col + offset)  # Top-right

    def add_move_if_valid(self, start_row, start_col, end_row, end_col):
        if 0 <= end_row < self.board.rows and 0 <= end_col < self.board.cols:
            is_valid, captures = self.validate_move(start_row, start_col, end_row, end_col)
            if is_valid:
                move_details = {
                    'start': (start_row, start_col),
                    'end': (end_row, end_col),
                    'captures': captures
                }
                # Add the move to capture_moves if it results in a capture, otherwise to possible_moves
                if captures:
                    self.capture_moves.append(move_details)
                else:
                    self.possible_moves.append(move_details)

    def validate_move(self, start_row, start_col, end_row, end_col):
        captures = []
        piece = self.board.get_piece(start_row, start_col)
        if not piece or piece.color != self.color:  # Only validate for pieces controlled by AI
            return False, captures

        is_valid, message = self.board.is_valid_move(piece, end_row, end_col)
        if is_valid:
            target_piece = self.board.get_piece(end_row, end_col)
            if target_piece and target_piece.color != self.color:
                captures.append((end_row, end_col))
            return True, captures

        return False, captures

    def select_and_execute_move(self):
        if not self.capture_moves and not self.possible_moves:
            #print("No possible moves to select from.")
            return

        # Prioritize capture moves if available
        if self.capture_moves:
            selected_move = random.choice(self.capture_moves)
        else:
            selected_move = random.choice(self.possible_moves)

        start = selected_move['start']
        end = selected_move['end']
        start_notation = self.proper_notation((start[1], start[0]))
        end_notation = self.proper_notation((end[1], end[0]))

        piece = self.board.get_piece(start[0], start[1])

        # If the move is valid
        if piece and self.board.is_valid_move(piece, end[0], end[1])[0]:

            # Process potential captures first
            if selected_move['captures']:
                for capture in selected_move['captures']:
                    captured_piece = self.board.get_piece(capture[0], capture[1])
                    if captured_piece:
                        self.board.remove_piece(captured_piece)
                        #print(f"Captured piece at {self.proper_notation((capture[1], capture[0]))}")

            # After handling captures, move the piece to its new position
            self.board.move_piece(piece, end[0], end[1])
            #print(f"AI moved from {start_notation} to {end_notation}")

        else:
            print(f"Failed to execute move: {start_notation} to {end_notation}")

    def make_move(self):
        self.generate_all_possible_moves()
        self.select_and_execute_move()
