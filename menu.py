import pygame
import random

class Menu:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 40)
        self.num_players = None  # Store the number of players
        self.players_type = []  # Store whether each player is Human or Computer
        self.board_size = None  # Store selected board size
        self.player_color = None  # To store the color assigned to the player
        self.computer_color = None  # To store the color assigned to the computer

        self.selection_phase = "num_players"  # To track the phase of selection
        self.transition_to_game = False  # Track when to transition to the game
        self.coin_flipping = False  # Track if the coin is flipping
        self.user_choice = None  # Store user's heads or tails selection
        self.coin_flip_result = None  # Store the final coin flip result

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
        elif self.selection_phase == "coin_toss":
            self.display_coin_toss()

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
        # If the user has not made a choice, let them select heads or tails
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

    def handle_click(self, pos):
        if self.selection_phase == "num_players":
            self.handle_num_players_click(pos)
        elif self.selection_phase == "player_type" and not self.transition_to_game:
            self.handle_player_type_click(pos)
        elif self.selection_phase == "board_size":
            self.handle_board_size_click(pos)
        elif self.selection_phase == "coin_toss":
            self.handle_coin_toss_click(pos)

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
                self.selection_phase = "coin_toss"  # Move to the coin toss phase

    def start_game(self):
        return self.transition_to_game
