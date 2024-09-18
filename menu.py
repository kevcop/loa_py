import pygame
import random
import math

class Menu:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 40)
        self.num_players = None  # Store the number of players
        self.players_type = []  # Store whether each player is Human or Computer
        self.board_size = None  # Store selected board size
        self.player_colors = None  # Store the color order for the players
        self.selection_phase = "num_players"  # To track the phase of selection
        self.transition_to_game = False  # Track when to transition to the game
        self.is_wheel_spinning = False  # Track if the wheel is spinning
        self.wheel_angle = 0  # Angle of the wheel rotation
        self.spin_speed = 0  # Speed at which the wheel spins
        self.center = (400, 400)  # Center of the wheel
        self.radius = 200  # Radius of the wheel
        self.winner = None  # To store which player goes first
        self.spin_order = []  # To store the final player order based on the wheel spin
        self.user_choice = None  # Track the user's heads/tails selection
        self.coin_flipping = False  # Track if the coin is flipping
        self.coin_flip_result = None  # Store the final coin flip result
        self.load_game_button_rect = pygame.Rect(300, 400, 200, 50)  # Load Game button
        self.selected_case = None  # Store the selected load game case

    def display(self):
        self.window.fill((240, 240, 240))

        # Display title
        title_surface = self.title_font.render("Lines of Action", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(400, 100))
        self.window.blit(title_surface, title_rect)

        if self.selection_phase == "num_players":
            self.display_num_players_selection()
        elif self.selection_phase == "player_type":
            self.display_player_type_selection()
        elif self.selection_phase == "board_size":
            self.display_board_size_selection()
        elif self.selection_phase == "coin_toss" and self.num_players == 2:
            self.display_coin_toss()  # Coin toss for 2 players remains unchanged
        elif self.selection_phase == "wheel_spin" and self.num_players == 4:
            self.display_wheel_spin()  # Wheel spin for 4 players
        elif self.selection_phase == "load_game":
            self.display_load_game_cases()  # Display load game cases

        pygame.display.flip()

    def display_num_players_selection(self):
        # Prompt to ask for number of players (2 or 4)
        prompt_surface = self.font.render("How many players? (2 or 4)", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(400, 200))
        self.window.blit(prompt_surface, prompt_rect)

        # Display options for players (2 or 4 players)
        for i, num in enumerate([2, 4]):
            option_surface = self.font.render(str(num), True, (0, 0, 0))
            option_rect = pygame.Rect(300 + i * 100, 250, 50, 50)
            pygame.draw.rect(self.window, (0, 0, 255), option_rect)
            option_surface_rect = option_surface.get_rect(center=option_rect.center)
            self.window.blit(option_surface, option_surface_rect)

        # Display the Load Game button
        pygame.draw.rect(self.window, (0, 0, 0), self.load_game_button_rect)
        load_game_surface = self.font.render("Load Game", True, (255, 255, 255))
        load_game_surface_rect = load_game_surface.get_rect(center=self.load_game_button_rect.center)
        self.window.blit(load_game_surface, load_game_surface_rect)

    def display_load_game_cases(self):
        # Display 5 "Case" buttons
        for i in range(5):
            button_rect = pygame.Rect(300, 200 + i * 60, 200, 50)
            pygame.draw.rect(self.window, (0, 0, 255), button_rect)
            case_surface = self.font.render(f"Case {i + 1}", True, (255, 255, 255))
            case_rect = case_surface.get_rect(center=button_rect.center)
            self.window.blit(case_surface, case_rect)

    def display_board_size_selection(self):
        # Prompt to ask for board size
        prompt_surface = self.font.render("Select board size:", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(400, 200))
        self.window.blit(prompt_surface, prompt_rect)

        # Display options for board size (8x8 only for 2 players, 12x12 or 16x16 for 4 players)
        sizes = [8, 12, 16] if self.num_players == 4 else [8]
        for i, size in enumerate(sizes):
            option_surface = self.font.render(f"{size} x {size}", True, (0, 0, 0))
            option_rect = pygame.Rect(300 + i * 100, 250, 100, 50)
            pygame.draw.rect(self.window, (0, 0, 255), option_rect)
            option_surface_rect = option_surface.get_rect(center=option_rect.center)
            self.window.blit(option_surface, option_surface_rect)

    def display_player_type_selection(self):
        # Prompt to ask if the player is human or computer
        current_player = len(self.players_type) + 1
        if current_player > self.num_players:
            self.selection_phase = "board_size"  # Move to board size selection phase
            return

        prompt_surface = self.font.render(f"Is Player {current_player} human or computer?", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(400, 200))
        self.window.blit(prompt_surface, prompt_rect)

        # Human and Computer buttons
        human_button_rect = pygame.Rect(250, 250, 150, 50)
        computer_button_rect = pygame.Rect(450, 250, 150, 50)

        pygame.draw.rect(self.window, (0, 255, 0), human_button_rect)  # Green for Human
        pygame.draw.rect(self.window, (255, 0, 0), computer_button_rect)  # Red for Computer

        human_surface = self.font.render("Human", True, (0, 0, 0))
        computer_surface = self.font.render("Computer", True, (0, 0, 0))

        self.window.blit(human_surface, human_button_rect.move(20, 10))
        self.window.blit(computer_surface, computer_button_rect.move(10, 10))

    def display_coin_toss(self):
        """Coin toss logic for 2 players."""
        if not self.user_choice:
            heads_button_rect = pygame.Rect(300, 300, 100, 50)
            tails_button_rect = pygame.Rect(450, 300, 100, 50)

            pygame.draw.rect(self.window, (0, 255, 0), heads_button_rect)
            pygame.draw.rect(self.window, (255, 0, 0), tails_button_rect)

            heads_surface = self.font.render("Heads", True, (0, 0, 0))
            tails_surface = self.font.render("Tails", True, (0, 0, 0))

            self.window.blit(heads_surface, heads_button_rect.move(10, 10))
            self.window.blit(tails_surface, tails_button_rect.move(10, 10))
        elif self.coin_flipping:
            # Simulate the coin flipping
            coin_side = random.choice(["Heads", "Tails"])
            result_surface = self.font.render(f"Coin is flipping: {coin_side}", True, (0, 0, 0))
            self.window.blit(result_surface, (300, 250))
            pygame.display.update()
            pygame.time.delay(300)

            if random.random() > 0.8:  # Random chance to stop flipping
                self.coin_flipping = False
                self.coin_flip_result = random.choice(["Heads", "Tails"])
        else:
            # Show the result of the coin flip
            result_text = f"The coin landed on {self.coin_flip_result.upper()}!"
            result_surface = self.font.render(result_text, True, (0, 0, 0))
            self.window.blit(result_surface, (300, 250))

            # Assign player and computer colors based on the result
            if self.user_choice == self.coin_flip_result:
                player_text = "You won the toss! You will play as BLACK."
                self.player_color = (0, 0, 0)  # Player gets black
                self.computer_color = (255, 255, 255)  # Computer gets white
            else:
                player_text = "You lost the toss! You will play as WHITE."
                self.player_color = (255, 255, 255)  # Player gets white
                self.computer_color = (0, 0, 0)  # Computer gets black

            # Display which color the user will play as
            player_surface = self.font.render(player_text, True, (0, 0, 0))
            self.window.blit(player_surface, (300, 300))

            # Transition to the game after a short delay
            pygame.display.update()
            pygame.time.wait(2000)
            self.transition_to_game = True

    def display_wheel_spin(self):
        """Handle 4-player wheel spin."""
        print(f"Wheel is spinning, speed: {self.spin_speed}, angle: {self.wheel_angle}")  # Debugging statement

        if not self.is_wheel_spinning:
            spin_button_rect = pygame.Rect(350, 550, 100, 50)
            pygame.draw.rect(self.window, (0, 255, 0), spin_button_rect)
            spin_text = self.font.render("Spin", True, (0, 0, 0))
            self.window.blit(spin_text, spin_button_rect.move(20, 10))
        else:
            # Draw the spinning wheel
            self.draw_wheel()

            # Simulate the wheel slowing down
            if self.spin_speed > 0:
                self.wheel_angle += self.spin_speed
                self.spin_speed *= 0.98  # Slowly reduce speed

                # Add a small threshold for stopping the wheel
                if self.spin_speed < 0.1:  # Adjust this value if necessary
                    self.spin_speed = 0  # Stop the wheel when it reaches a small speed value
            else:
                print("Wheel spin completed, determining winner...")  # Debugging statement
                self.is_wheel_spinning = False
                self.determine_winner()  # Determine who goes first and assign colors

    def draw_wheel(self):
        """Draw the wheel with 4 sections labeled 1, 2, 3, 4 for the players."""
        num_sections = 4  # Number of sections on the wheel
        section_colors = [(200, 200, 200), (150, 150, 150), (100, 100, 100), (50, 50, 50)]  # Greyscale for visual clarity
        section_labels = ["1", "2", "3", "4"]  # Player labels

        for i in range(num_sections):
            start_angle = i * (360 // num_sections)
            end_angle = (i + 1) * (360 // num_sections)

            # Draw the wheel sections in different shades of grey
            pygame.draw.polygon(self.window, section_colors[i],
                                self.get_wheel_section_points(start_angle, end_angle))

            # Display player numbers on each section
            text_surface = self.font.render(section_labels[i], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.get_wheel_section_center(start_angle, end_angle))
            self.window.blit(text_surface, text_rect)

        # Draw an arrow indicator pointing to the current section
        self.draw_wheel_arrow()

    def get_wheel_section_points(self, start_angle, end_angle):
        """Calculate the points for each section of the wheel."""
        points = [self.center]  # Start with the center of the wheel
        for angle in (start_angle, end_angle):
            x = self.center[0] + self.radius * math.cos(math.radians(angle + self.wheel_angle))
            y = self.center[1] + self.radius * math.sin(math.radians(angle + self.wheel_angle))
            points.append((x, y))
        return points

    def get_wheel_section_center(self, start_angle, end_angle):
        """Calculate the center point of each wheel section."""
        mid_angle = (start_angle + end_angle) / 2
        x = self.center[0] + self.radius / 1.5 * math.cos(math.radians(mid_angle + self.wheel_angle))
        y = self.center[1] + self.radius / 1.5 * math.sin(math.radians(mid_angle + self.wheel_angle))
        return (x, y)

    def draw_wheel_arrow(self):
        """Draw an arrow pointing to the section that the wheel stops on."""
        arrow_points = [
            (self.center[0] - 10, self.center[1] - self.radius - 10),
            (self.center[0] + 10, self.center[1] - self.radius - 10),
            (self.center[0], self.center[1] - self.radius)
        ]
        pygame.draw.polygon(self.window, (255, 0, 0), arrow_points)

    def determine_winner(self):
        print("Determining player colors based on wheel spin...")

        section = int(self.wheel_angle % 360 // (360 // 4)) + 1
        self.winner = section
        print(f"Wheel stopped at section: {section}")  # Debugging the wheel outcome

        # Assign players to colors based on the result of the spin
        if self.winner == 1:
            self.player_colors = {1: (0, 0, 0), 2: (255, 255, 255), 3: (255, 0, 0), 4: (0, 255, 0)}
        elif self.winner == 2:
            self.player_colors = {2: (0, 0, 0), 3: (255, 255, 255), 4: (255, 0, 0), 1: (0, 255, 0)}
        elif self.winner == 3:
            self.player_colors = {3: (0, 0, 0), 4: (255, 255, 255), 1: (255, 0, 0), 2: (0, 255, 0)}
        elif self.winner == 4:
            self.player_colors = {4: (0, 0, 0), 1: (255, 255, 255), 2: (255, 0, 0), 3: (0, 255, 0)}

        print(f"Player colors assigned: {self.player_colors}")  # Debugging player color assignment

        # Transition to the game
        pygame.time.wait(2000)
        print("Transitioning to game...")  # Debugging transition flag
        self.transition_to_game = True

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

        # Handle Load Game button click
        if self.selection_phase == "num_players" and self.load_game_button_rect.collidepoint(pos):
            self.selection_phase = "load_game"  # Move to the load game phase

    def handle_load_game_click(self, pos):
        # Check which "Case" button is clicked
        for i in range(5):
            button_rect = pygame.Rect(300, 200 + i * 60, 200, 50)
            if button_rect.collidepoint(pos):
                # Store the selected case number
                self.selected_case = i + 1
                print(f"Load Game: Case {self.selected_case} selected")  # For debugging
                self.transition_to_game = True  # Transition to the game

    def handle_wheel_spin_click(self, pos):
        """Handle spinning the wheel when the user clicks the spin button."""
        spin_button_rect = pygame.Rect(350, 550, 100, 50)

        if spin_button_rect.collidepoint(pos) and not self.is_wheel_spinning:
            self.is_wheel_spinning = True
            self.spin_speed = random.randint(10, 15)  # Random spin speed

    def handle_num_players_click(self, pos):
        for i, num in enumerate([2, 4]):
            option_rect = pygame.Rect(300 + i * 100, 250, 50, 50)
            if option_rect.collidepoint(pos):
                self.num_players = num
                self.selection_phase = "player_type"  # Move to player type selection

    def handle_player_type_click(self, pos):
        human_button_rect = pygame.Rect(250, 250, 150, 50)
        computer_button_rect = pygame.Rect(450, 250, 150, 50)

        if human_button_rect.collidepoint(pos):
            self.players_type.append("Human")
        elif computer_button_rect.collidepoint(pos):
            self.players_type.append("Computer")

        # Move to the next player or start the game
        if len(self.players_type) >= self.num_players:
            self.selection_phase = "board_size"

    def handle_board_size_click(self, pos):
        sizes = [8, 12, 16] if self.num_players == 4 else [8]
        for i, size in enumerate(sizes):
            option_rect = pygame.Rect(300 + i * 100, 250, 100, 50)
            if option_rect.collidepoint(pos):
                self.board_size = size
                # Move to the next phase based on number of players
                self.selection_phase = "coin_toss" if self.num_players == 2 else "wheel_spin"

    def start_game(self):
        """Transition to game, returning necessary values."""
        if self.transition_to_game:
            if self.selected_case:  # If a case was selected for loading
                return {
                    'num_players': 2,
                    'players_type': ["Human", "Computer"],
                    'board_size': 8,  # Assuming default board size for loaded games
                    'player_order': None,  # Not needed for 2-player mode
                    'player_colors': None,  # Not needed for 2-player mode
                    'case': self.selected_case  # Pass the selected case
                }
            elif self.num_players == 2:
                # Return settings for a 2-player game
                return {
                    'num_players': self.num_players,
                    'players_type': self.players_type,
                    'board_size': self.board_size,
                    'player_color': self.player_color,
                    'computer_color': self.computer_color,
                    'player_order': None,  # Not used for 2-player mode
                    'player_colors': None  # Not used for 2-player mode
                }
            else:
                # Return settings for a 4-player game
                return {
                    'num_players': self.num_players,
                    'players_type': self.players_type,
                    'player_order': self.spin_order,
                    'player_colors': self.player_colors,
                    'board_size': self.board_size
                }
        return None

    def handle_coin_toss_click(self, pos):
        # Handle the user selecting heads or tails
        heads_button_rect = pygame.Rect(300, 300, 100, 50)
        tails_button_rect = pygame.Rect(450, 300, 100, 50)

        if heads_button_rect.collidepoint(pos) and not self.user_choice:
            self.user_choice = "Heads"
            self.coin_flipping = True
        elif tails_button_rect.collidepoint(pos) and not self.user_choice:
            self.user_choice = "Tails"
            self.coin_flipping = True

    def start_loaded_game(self):
        """Setup and start the game with the loaded state."""
        if self.selected_case:
            return {
                'num_players': 2,
                'players_type': ["Human", "Computer"],
                'board_size': 8,  # Assuming default board size for loaded games
                'player_order': None,
                'player_colors': None,
                'case': self.selected_case  # Load the specified game case
            }
        return None
