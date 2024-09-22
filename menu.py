import pygame
import random
import math


class Menu:
    """
    A class to represent the game menu where players select settings for the game.

    Attributes:
        window (pygame.Surface): The pygame window where the menu will be drawn.
        font (pygame.font.Font): Font for rendering menu text.
        title_font (pygame.font.Font): Font for rendering the game title.
        num_players (int or None): The number of players chosen.
        players_type (list): List storing whether each player is human or computer.
        board_size (int or None): The size of the game board.
        player_colors (dict or None): The color order for the players.
        selection_phase (str): Tracks which menu selection phase is currently active.
        transition_to_game (bool): Indicates whether to transition to the game.
        is_wheel_spinning (bool): Tracks whether the wheel is spinning.
        wheel_angle (float): The current angle of the spinning wheel.
        spin_speed (float): The speed of the wheel spin.
        center (tuple): The center point of the wheel.
        radius (int): The radius of the wheel.
        winner (int or None): The player who wins the wheel spin.
        spin_order (list): The final order of players based on the wheel spin.
        user_choice (str or None): The user's heads/tails choice for the coin toss.
        coin_flipping (bool): Tracks whether the coin is flipping.
        coin_flip_result (str or None): The result of the coin flip.
        load_game_button_rect (pygame.Rect): Rectangle representing the Load Game button.
        selected_case (int or None): The selected case for loading a saved game.
    """

    def __init__(self, window):
        """
        Initializes the Menu object.

        Args:
            window (pygame.Surface): The pygame window where the menu will be drawn.
        """
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

    def display(self):
        """
        Displays the appropriate menu screen based on the current selection phase.
        """
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

    def display_num_players_selection(self):
        """
        Displays the selection options for the number of players (2 or 4).
        """
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

    def display_load_game_cases(self):
        """
        Displays the available saved game cases to load.
        """
        for i in range(5):
            button_rect = pygame.Rect(300, 200 + i * 60, 200, 50)
            pygame.draw.rect(self.window, (0, 0, 255), button_rect)
            case_surface = self.font.render(f"Case {i + 1}", True, (255, 255, 255))
            case_rect = case_surface.get_rect(center=button_rect.center)
            self.window.blit(case_surface, case_rect)

    def display_board_size_selection(self):
        """
        Displays the selection options for the board size.
        """
        prompt_surface = self.font.render("Select board size:", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(400, 200))
        self.window.blit(prompt_surface, prompt_rect)

        # Allow only 12x12 and 16x16 for 4 players, and all sizes for 2 players
        sizes = [12, 16] if self.num_players == 4 else [8]

        for i, size in enumerate(sizes):
            option_surface = self.font.render(f"{size} x {size}", True, (0, 0, 0))
            option_rect = pygame.Rect(300 + i * 100, 250, 100, 50)
            pygame.draw.rect(self.window, (0, 0, 255), option_rect)
            option_surface_rect = option_surface.get_rect(center=option_rect.center)
            self.window.blit(option_surface, option_surface_rect)

    def display_player_type_selection(self):
        """
        Displays the selection options for whether each player is human or computer.
        """
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

    def display_coin_toss(self):
        """
        Displays the coin toss option for a 2-player game, showing who will play as Black and start first.
        """
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

            # Shortened and broken up to ensure it fits on the screen
            player_surface = self.font.render(player_text, True, (0, 0, 0))
            player_surface_line_1 = self.font.render(
                "Player 1" if self.user_choice == self.coin_flip_result else "Player 2", True, (0, 0, 0))
            player_surface_line_2 = self.font.render("will play as Black and go first.", True, (0, 0, 0))

            self.window.blit(player_surface_line_1, (300, 300))
            self.window.blit(player_surface_line_2, (300, 350))

            pygame.display.update()
            pygame.time.wait(2000)

            # Transition to the game after the coin toss result
            self.transition_to_game = True

    def display_wheel_spin(self):
        """
        Displays and manages the 4-player wheel spin.
        """
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

    def draw_wheel(self):
        """
        Draws the wheel with 4 sections representing the players.
        """
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

    def get_wheel_section_points(self, start_angle, end_angle):
        """
        Returns the polygon points for a section of the wheel.

        Args:
            start_angle (int): The starting angle of the section.
            end_angle (int): The ending angle of the section.

        Returns:
            list of tuples: The points of the section.
        """
        points = [self.center]
        for angle in (start_angle, end_angle):
            x = self.center[0] + self.radius * math.cos(math.radians(angle + self.wheel_angle))
            y = self.center[1] + self.radius * math.sin(math.radians(angle + self.wheel_angle))
            points.append((x, y))
        return points

    def get_wheel_section_center(self, start_angle, end_angle):
        """
        Calculates the center of a wheel section.

        Args:
            start_angle (int): The starting angle of the section.
            end_angle (int): The ending angle of the section.

        Returns:
            tuple: The center point of the section.
        """
        mid_angle = (start_angle + end_angle) / 2
        x = self.center[0] + self.radius / 1.5 * math.cos(math.radians(mid_angle + self.wheel_angle))
        y = self.center[1] + self.radius / 1.5 * math.sin(math.radians(mid_angle + self.wheel_angle))
        return (x, y)

    def draw_wheel_arrow(self):
        """
        Draws an arrow pointing at the current wheel section.
        """
        arrow_points = [
            (self.center[0] - 10, self.center[1] - self.radius - 10),
            (self.center[0] + 10, self.center[1] - self.radius - 10),
            (self.center[0], self.center[1] - self.radius)
        ]
        pygame.draw.polygon(self.window, (255, 0, 0), arrow_points)

    def determine_winner(self):
        """
        Determines the winner based on the final wheel position.
        """
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

    def handle_click(self, pos):
        """
        Handles mouse clicks on the menu buttons.

        Args:
            pos (tuple): The (x, y) position of the mouse click.
        """
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

    def handle_load_game_click(self, pos):
        """
        Handles clicks on the Load Game case buttons.

        Args:
            pos (tuple): The (x, y) position of the mouse click.
        """
        for i in range(5):
            button_rect = pygame.Rect(300, 200 + i * 60, 200, 50)
            if button_rect.collidepoint(pos):
                self.selected_case = i + 1
                self.transition_to_game = True

    def handle_wheel_spin_click(self, pos):
        """
        Handles clicks on the "Spin" button to start the wheel spin.

        Args:
            pos (tuple): The (x, y) position of the mouse click.
        """
        spin_button_rect = pygame.Rect(350, 550, 100, 50)

        if spin_button_rect.collidepoint(pos) and not self.is_wheel_spinning:
            self.is_wheel_spinning = True
            self.spin_speed = random.randint(10, 15)

    def handle_num_players_click(self, pos):
        """
        Handles clicks on the number of players options.

        Args:
            pos (tuple): The (x, y) position of the mouse click.
        """
        for i, num in enumerate([2, 4]):
            option_rect = pygame.Rect(300 + i * 100, 250, 50, 50)
            if option_rect.collidepoint(pos):
                self.num_players = num
                self.selection_phase = "player_type"

    def handle_player_type_click(self, pos):
        """
        Handles clicks on the player type options (Human or Computer).

        Args:
            pos (tuple): The (x, y) position of the mouse click.
        """
        human_button_rect = pygame.Rect(250, 250, 150, 50)
        computer_button_rect = pygame.Rect(450, 250, 150, 50)

        if human_button_rect.collidepoint(pos):
            self.players_type.append("Human")
        elif computer_button_rect.collidepoint(pos):
            self.players_type.append("Computer")

        if len(self.players_type) >= self.num_players:
            self.selection_phase = "board_size"

    def handle_board_size_click(self, pos):
        """
        Handles clicks on the board size options.

        Args:
            pos (tuple): The (x, y) position of the mouse click.
        """
        sizes = [12, 16] if self.num_players == 4 else [8,12,16]
        for i, size in enumerate(sizes):
            option_rect = pygame.Rect(300 + i * 100, 250, 100, 50)
            if option_rect.collidepoint(pos):
                self.board_size = size
                self.selection_phase = "coin_toss" if self.num_players == 2 else "wheel_spin"

    def start_game(self):
        """
        Returns the necessary settings to start the game.

        Returns:
            dict: Game settings based on user input.
        """
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

    def handle_coin_toss_click(self, pos):
        """
        Handles the user selection of heads or tails for the coin toss.

        Args:
            pos (tuple): The (x, y) position of the mouse click.
        """
        heads_button_rect = pygame.Rect(300, 300, 100, 50)
        tails_button_rect = pygame.Rect(450, 300, 100, 50)

        if heads_button_rect.collidepoint(pos) and not self.user_choice:
            self.user_choice = "Heads"
            self.coin_flipping = True
        elif tails_button_rect.collidepoint(pos) and not self.user_choice:
            self.user_choice = "Tails"
            self.coin_flipping = True

    def start_loaded_game(self):
        """
        Sets up and returns the game settings for a loaded game.

        Returns:
            dict: Settings for the loaded game.
        """
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
