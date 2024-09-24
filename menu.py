import pygame
import random
import math

class Menu:
    """
    A class to represent the game menu where players select settings for the game.
    """

    """
    Function Name: __init__
    Purpose: To initialize the Menu object with the pygame window and default settings.
    Parameters:
        window (pygame.Surface): The pygame window where the menu will be drawn.
    Return Value: None
    Algorithm:
        1) Set up default values for the menu attributes, including window, fonts, player options, and game settings.
    Reference: None
    """
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 40)
        self.num_players = None
        self.players_type = []
        self.board_size = None
        self.player_colors = None
        self.selection_phase = "num_players"
        self.transition_to_game = False
        self.is_wheel_spinning = False
        self.wheel_angle = 0
        self.spin_speed = 0
        self.center = (400, 400)
        self.radius = 200
        self.winner = None
        self.spin_order = []
        self.user_choice = None
        self.coin_flipping = False
        self.coin_flip_result = None
        self.load_game_button_rect = pygame.Rect(300, 400, 200, 50)
        self.selected_case = None

    """
    Function Name: display
    Purpose: To display the appropriate menu screen based on the current selection phase.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Fill the screen with a background color.
        2) Display the game title and options based on the current selection phase.
    Reference: None
    """
    def display(self):
        self.window.fill((240, 240, 240))

        # Display the game title.
        title_surface = self.title_font.render("Lines of Action", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(400, 100))
        self.window.blit(title_surface, title_rect)

        # Display the menu options based on the selection phase.
        if self.selection_phase == "num_players":
            self.display_num_players_selection()
        elif self.selection_phase == "player_type":
            self.display_player_type_selection()
        elif self.selection_phase == "board_size":
            self.display_board_size_selection()
        elif self.selection_phase == "coin_toss" and self.num_players == 2:
            self.display_coin_toss()
        elif self.selection_phase == "wheel_spin" and self.num_players == 4:
            self.display_wheel_spin()
        elif self.selection_phase == "load_game":
            self.display_load_game_cases()

        pygame.display.flip()

    """
    Function Name: display_num_players_selection
    Purpose: To display the selection options for the number of players (2 or 4).
    Parameters: None
    Return Value: None
    Algorithm:
        1) Render the prompt asking how many players, and display clickable options for 2 or 4 players.
        2) Draw the Load Game button.
    Reference: None
    """
    def display_num_players_selection(self):
        prompt_surface = self.font.render("How many players? (2 or 4)", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(400, 200))
        self.window.blit(prompt_surface, prompt_rect)

        for i, num in enumerate([2, 4]):
            option_surface = self.font.render(str(num), True, (0, 0, 0))
            option_rect = pygame.Rect(300 + i * 100, 250, 50, 50)
            pygame.draw.rect(self.window, (0, 0, 255), option_rect)
            option_surface_rect = option_surface.get_rect(center=option_rect.center)
            self.window.blit(option_surface, option_surface_rect)

        # Draw the "Load Game" button.
        pygame.draw.rect(self.window, (0, 0, 0), self.load_game_button_rect)
        load_game_surface = self.font.render("Load Game", True, (255, 255, 255))
        load_game_surface_rect = load_game_surface.get_rect(center=self.load_game_button_rect.center)
        self.window.blit(load_game_surface, load_game_surface_rect)

    """
    Function Name: display_load_game_cases
    Purpose: To display the available saved game cases for loading a game.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Loop through available saved game cases and display them as clickable buttons.
    Reference: None
    """
    def display_load_game_cases(self):
        for i in range(5):
            button_rect = pygame.Rect(300, 200 + i * 60, 200, 50)
            pygame.draw.rect(self.window, (0, 0, 255), button_rect)
            case_surface = self.font.render(f"Case {i + 1}", True, (255, 255, 255))
            case_rect = case_surface.get_rect(center=button_rect.center)
            self.window.blit(case_surface, case_rect)

    """
    Function Name: display_board_size_selection
    Purpose: To display the selection options for the board size.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Render the prompt asking the player to select the board size.
        2) Display clickable options for board sizes (depending on player count).
    Reference: None
    """
    def display_board_size_selection(self):
        prompt_surface = self.font.render("Select board size:", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(400, 200))
        self.window.blit(prompt_surface, prompt_rect)

        sizes = [12, 16] if self.num_players == 4 else [8]

        for i, size in enumerate(sizes):
            option_surface = self.font.render(f"{size} x {size}", True, (0, 0, 0))
            option_rect = pygame.Rect(300 + i * 100, 250, 100, 50)
            pygame.draw.rect(self.window, (0, 0, 255), option_rect)
            option_surface_rect = option_surface.get_rect(center=option_rect.center)
            self.window.blit(option_surface, option_surface_rect)

    """
    Function Name: display_player_type_selection
    Purpose: To display the selection options for whether each player is human or computer.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Render the prompt asking if the current player is human or computer.
        2) Display clickable buttons for "Human" or "Computer".
    Reference: None
    """
    def display_player_type_selection(self):
        current_player = len(self.players_type) + 1
        if current_player > self.num_players:
            self.selection_phase = "board_size"
            return

        prompt_surface = self.font.render(f"Is Player {current_player} human or computer?", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(400, 200))
        self.window.blit(prompt_surface, prompt_rect)

        human_button_rect = pygame.Rect(250, 250, 150, 50)
        computer_button_rect = pygame.Rect(450, 250, 150, 50)

        pygame.draw.rect(self.window, (0, 255, 0), human_button_rect)
        pygame.draw.rect(self.window, (255, 0, 0), computer_button_rect)

        human_surface = self.font.render("Human", True, (0, 0, 0))
        computer_surface = self.font.render("Computer", True, (0, 0, 0))

        self.window.blit(human_surface, human_button_rect.move(20, 10))
        self.window.blit(computer_surface, computer_button_rect.move(10, 10))

    """
    Function Name: display_coin_toss
    Purpose: To display the coin toss option for a 2-player game, showing who will play as Black and start first.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Display heads and tails buttons for the user to pick.
        2) Simulate and display the coin toss result.
    Reference: None
    """
    def display_coin_toss(self):
        if not self.user_choice:
            # Display heads and tails buttons for user to pick
            heads_button_rect = pygame.Rect(300, 300, 100, 50)
            tails_button_rect = pygame.Rect(450, 300, 100, 50)

            pygame.draw.rect(self.window, (0, 255, 0), heads_button_rect)
            pygame.draw.rect(self.window, (255, 0, 0), tails_button_rect)

            heads_surface = self.font.render("Heads", True, (0, 0, 0))
            tails_surface = self.font.render("Tails", True, (0, 0, 0))

            self.window.blit(heads_surface, heads_button_rect.move(10, 10))
            self.window.blit(tails_surface, tails_button_rect.move(10, 10))

        elif self.coin_flipping:
            # Simulate coin flipping
            coin_side = random.choice(["Heads", "Tails"])
            result_surface = self.font.render(f"Coin is flipping: {coin_side}", True, (0, 0, 0))
            self.window.blit(result_surface, (300, 250))
            pygame.display.update()
            pygame.time.delay(300)

            # Stop flipping the coin after a certain time
            if random.random() > 0.8:
                self.coin_flipping = False
                self.coin_flip_result = random.choice(["Heads", "Tails"])

        else:
            # Display the coin flip result
            result_text = f"The coin landed on {self.coin_flip_result.upper()}!"
            result_surface = self.font.render(result_text, True, (0, 0, 0))
            self.window.blit(result_surface, (300, 250))

            # Determine who will play as Black and go first
            if self.user_choice == self.coin_flip_result:
                player_text = "Player 1 will play as Black and go first."
                self.player_color = (0, 0, 0)
                self.computer_color = (255, 255, 255)
            else:
                player_text = "Player 2 will play as Black and go first."
                self.player_color = (255, 255, 255)
                self.computer_color = (0, 0, 0)

            player_surface = self.font.render(player_text, True, (0, 0, 0))
            self.window.blit(player_surface, (300, 300))

            pygame.display.update()
            pygame.time.wait(2000)

            # Transition to the game after the coin toss result
            self.transition_to_game = True

    """
    Function Name: display_wheel_spin
    Purpose: To display and manage the 4-player wheel spin.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Render a spinning wheel and allow players to spin to determine the starting order.
    Reference: None
    """
    def display_wheel_spin(self):
        if not self.is_wheel_spinning:
            spin_button_rect = pygame.Rect(350, 550, 100, 50)
            pygame.draw.rect(self.window, (0, 255, 0), spin_button_rect)
            spin_text = self.font.render("Spin", True, (0, 0, 0))
            self.window.blit(spin_text, spin_button_rect.move(20, 10))
        else:
            self.draw_wheel()
            if self.spin_speed > 0:
                self.wheel_angle += self.spin_speed
                self.spin_speed *= 0.98
                if self.spin_speed < 0.1:
                    self.spin_speed = 0
            else:
                self.is_wheel_spinning = False
                self.determine_winner()

    """
    Function Name: draw_wheel
    Purpose: To draw the wheel with 4 sections representing the players.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Render a spinning wheel divided into 4 sections, each representing a player.
    Reference: None
    """
    def draw_wheel(self):
        num_sections = 4
        section_colors = [(200, 200, 200), (150, 150, 150), (100, 100, 100), (50, 50, 50)]
        section_labels = ["1", "2", "3", "4"]

        for i in range(num_sections):
            start_angle = i * (360 // num_sections)
            end_angle = (i + 1) * (360 // num_sections)
            pygame.draw.polygon(self.window, section_colors[i],
                                self.get_wheel_section_points(start_angle, end_angle))

            text_surface = self.font.render(section_labels[i], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.get_wheel_section_center(start_angle, end_angle))
            self.window.blit(text_surface, text_rect)

        self.draw_wheel_arrow()

    """
    Function Name: get_wheel_section_points
    Purpose: To calculate and return the points for a section of the wheel.
    Parameters:
        start_angle (int): The starting angle of the section.
        end_angle (int): The ending angle of the section.
    Return Value: list of tuples: The points of the section.
    Algorithm:
        1) Calculate the x and y coordinates of the section's boundary points using trigonometry.
    Reference: None
    """
    def get_wheel_section_points(self, start_angle, end_angle):
        points = [self.center]
        for angle in (start_angle, end_angle):
            x = self.center[0] + self.radius * math.cos(math.radians(angle + self.wheel_angle))
            y = self.center[1] + self.radius * math.sin(math.radians(angle + self.wheel_angle))
            points.append((x, y))
        return points

    """
    Function Name: get_wheel_section_center
    Purpose: To calculate the center point of a wheel section.
    Parameters:
        start_angle (int): The starting angle of the section.
        end_angle (int): The ending angle of the section.
    Return Value: tuple: The center point of the section.
    Algorithm:
        1) Use trigonometry to calculate the midpoint angle and then the x and y coordinates.
    Reference: None
    """
    def get_wheel_section_center(self, start_angle, end_angle):
        mid_angle = (start_angle + end_angle) / 2
        x = self.center[0] + self.radius / 1.5 * math.cos(math.radians(mid_angle + self.wheel_angle))
        y = self.center[1] + self.radius / 1.5 * math.sin(math.radians(mid_angle + self.wheel_angle))
        return (x, y)

    """
    Function Name: draw_wheel_arrow
    Purpose: To draw an arrow pointing at the current section of the wheel.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Draw a triangular arrow at the top of the wheel, indicating the selected section.
    Reference: None
    """
    def draw_wheel_arrow(self):
        arrow_points = [
            (self.center[0] - 10, self.center[1] - self.radius - 10),
            (self.center[0] + 10, self.center[1] - self.radius - 10),
            (self.center[0], self.center[1] - self.radius)
        ]
        pygame.draw.polygon(self.window, (255, 0, 0), arrow_points)

    """
    Function Name: determine_winner
    Purpose: To determine the winner based on the final wheel position.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Use the wheel angle to determine which section the arrow is pointing to.
        2) Assign the winning player and set the colors based on the winner.
    Reference: None
    """
    def determine_winner(self):
        section = int(self.wheel_angle % 360 // (360 // 4)) + 1
        self.winner = section

        if self.winner == 1:
            self.player_colors = {1: (0, 0, 0), 2: (255, 255, 255), 3: (255, 0, 0), 4: (0, 255, 0)}
        elif self.winner == 2:
            self.player_colors = {2: (0, 0, 0), 3: (255, 255, 255), 4: (255, 0, 0), 1: (0, 255, 0)}
        elif self.winner == 3:
            self.player_colors = {3: (0, 0, 0), 4: (255, 255, 255), 1: (255, 0, 0), 2: (0, 255, 0)}
        elif self.winner == 4:
            self.player_colors = {4: (0, 0, 0), 1: (255, 255, 255), 2: (255, 0, 0), 3: (0, 255, 0)}

        pygame.time.wait(2000)
        self.transition_to_game = True

    """
    Function Name: handle_click
    Purpose: Handles mouse clicks on the menu buttons and determines which phase of the selection process to handle.
    Parameters:
        pos (tuple): The (x, y) position of the mouse click.
    Return Value: None
    Algorithm:
        1) Check the current selection phase and call the corresponding handler.
        2) Handle clicks for each selection phase like number of players, player type, board size, etc.
    Reference: None
    """
    def handle_click(self, pos):
        if self.selection_phase == "num_players":
            self.handle_num_players_click(pos)
        elif self.selection_phase == "player_type" and not self.transition_to_game:
            self.handle_player_type_click(pos)
        elif self.selection_phase == "board_size":
            self.handle_board_size_click(pos)
        elif self.selection_phase == "coin_toss":
            self.handle_coin_toss_click(pos)
        elif self.selection_phase == "wheel_spin":
            self.handle_wheel_spin_click(pos)
        elif self.selection_phase == "load_game":
            self.handle_load_game_click(pos)

        if self.selection_phase == "num_players" and self.load_game_button_rect.collidepoint(pos):
            self.selection_phase = "load_game"

    """
    Function Name: handle_load_game_click
    Purpose: Handles clicks on the Load Game case buttons to select a saved game.
    Parameters:
        pos (tuple): The (x, y) position of the mouse click.
    Return Value: None
    Algorithm:
        1) Loop through available saved game cases.
        2) Check if the user clicked one of the available saved game cases and transition to the game.
    Reference: None
    """
    def handle_load_game_click(self, pos):
        for i in range(5):
            button_rect = pygame.Rect(300, 200 + i * 60, 200, 50)
            if button_rect.collidepoint(pos):
                self.selected_case = i + 1
                self.transition_to_game = True

    """
    Function Name: handle_wheel_spin_click
    Purpose: Handles clicks on the "Spin" button to start the wheel spin.
    Parameters:
        pos (tuple): The (x, y) position of the mouse click.
    Return Value: None
    Algorithm:
        1) Check if the spin button was clicked.
        2) If clicked and the wheel is not already spinning, start the wheel spin with a random speed.
    Reference: None
    """
    def handle_wheel_spin_click(self, pos):
        spin_button_rect = pygame.Rect(350, 550, 100, 50)

        if spin_button_rect.collidepoint(pos) and not self.is_wheel_spinning:
            self.is_wheel_spinning = True
            self.spin_speed = random.randint(10, 15)

    """
    Function Name: handle_num_players_click
    Purpose: Handles clicks on the number of players options.
    Parameters:
        pos (tuple): The (x, y) position of the mouse click.
    Return Value: None
    Algorithm:
        1) Check if the user clicked on the number of players (2 or 4) and store the choice.
        2) Transition to the player type selection phase.
    Reference: None
    """
    def handle_num_players_click(self, pos):
        for i, num in enumerate([2, 4]):
            option_rect = pygame.Rect(300 + i * 100, 250, 50, 50)
            if option_rect.collidepoint(pos):
                self.num_players = num
                self.selection_phase = "player_type"

    """
    Function Name: handle_player_type_click
    Purpose: Handles clicks on the player type options (Human or Computer).
    Parameters:
        pos (tuple): The (x, y) position of the mouse click.
    Return Value: None
    Algorithm:
        1) Check if the user clicked on "Human" or "Computer" for each player.
        2) Append the selection to the players_type list.
        3) Move to the board size selection phase after all players are chosen.
    Reference: None
    """
    def handle_player_type_click(self, pos):
        human_button_rect = pygame.Rect(250, 250, 150, 50)
        computer_button_rect = pygame.Rect(450, 250, 150, 50)

        if human_button_rect.collidepoint(pos):
            self.players_type.append("Human")
        elif computer_button_rect.collidepoint(pos):
            self.players_type.append("Computer")

        if len(self.players_type) >= self.num_players:
            self.selection_phase = "board_size"

    """
    Function Name: handle_board_size_click
    Purpose: Handles clicks on the board size options.
    Parameters:
        pos (tuple): The (x, y) position of the mouse click.
    Return Value: None
    Algorithm:
        1) Check if the user clicked on one of the available board size options.
        2) Store the selected board size and transition to the next phase (coin toss or wheel spin).
    Reference: None
    """
    def handle_board_size_click(self, pos):
        sizes = [12, 16] if self.num_players == 4 else [8, 12, 16]
        for i, size in enumerate(sizes):
            option_rect = pygame.Rect(300 + i * 100, 250, 100, 50)
            if option_rect.collidepoint(pos):
                self.board_size = size
                self.selection_phase = "coin_toss" if self.num_players == 2 else "wheel_spin"

    """
    Function Name: start_game
    Purpose: Returns the necessary settings to start the game.
    Parameters: None
    Return Value: dict: Game settings based on user input.
    Algorithm:
        1) If transitioning to the game, return the settings for a new or loaded game.
        2) Set up the number of players, player types, board size, player colors, and any loaded game case.
    Reference: None
    """
    def start_game(self):
        if self.transition_to_game:
            if self.selected_case:
                return {
                    'num_players': 2,
                    'players_type': ["Human", "Computer"],
                    'board_size': 8,
                    'player_order': None,
                    'player_colors': None,
                    'case': self.selected_case
                }
            elif self.num_players == 2:
                return {
                    'num_players': self.num_players,
                    'players_type': self.players_type,
                    'board_size': self.board_size,
                    'player_color': self.player_color,
                    'computer_color': self.computer_color,
                    'player_order': None,
                    'player_colors': None
                }
            else:
                return {
                    'num_players': self.num_players,
                    'players_type': self.players_type,
                    'player_order': self.spin_order,
                    'player_colors': self.player_colors,
                    'board_size': self.board_size
                }
        return None

    """
    Function Name: handle_coin_toss_click
    Purpose: Handles the user selection of heads or tails for the coin toss.
    Parameters:
        pos (tuple): The (x, y) position of the mouse click.
    Return Value: None
    Algorithm:
        1) Check if the user clicked "Heads" or "Tails" and store the choice.
        2) Start flipping the coin after a selection is made.
    Reference: None
    """
    def handle_coin_toss_click(self, pos):
        heads_button_rect = pygame.Rect(300, 300, 100, 50)
        tails_button_rect = pygame.Rect(450, 300, 100, 50)

        if heads_button_rect.collidepoint(pos) and not self.user_choice:
            self.user_choice = "Heads"
            self.coin_flipping = True
        elif tails_button_rect.collidepoint(pos) and not self.user_choice:
            self.user_choice = "Tails"
            self.coin_flipping = True

    """
    Function Name: start_loaded_game
    Purpose: Sets up and returns the game settings for a loaded game.
    Parameters: None
    Return Value: dict: Settings for the loaded game.
    Algorithm:
        1) Return the settings for a loaded game including the number of players, player types, board size, and selected case.
    Reference: None
    """
    def start_loaded_game(self):
        if self.selected_case:
            return {
                'num_players': 2,
                'players_type': ["Human", "Computer"],
                'board_size': 8,
                'player_order': None,
                'player_colors': None,
                'case': self.selected_case
            }
        return None

