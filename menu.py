# menu.py

import pygame

class Menu:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 40)
        self.num_players = None  # Store the number of players
        self.players_type = []  # Store whether each player is Human or Computer

        self.start_button_rect = pygame.Rect(300, 400, 200, 50)  # Start button
        self.selection_phase = "num_players"  # To track the phase of selection ("num_players" or "player_type")
        self.transition_to_game = False  # Track when to transition to the game

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

        pygame.display.flip()

    def display_num_players_selection(self):
        # Prompt to ask for number of players
        prompt_surface = self.font.render("How many players? (2-4)", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(400, 200))
        self.window.blit(prompt_surface, prompt_rect)

        # Display number options (2-4 players)
        for i in range(2, 5):
            option_surface = self.font.render(str(i), True, (0, 0, 0))
            option_rect = pygame.Rect(300 + (i - 2) * 100, 250, 50, 50)
            pygame.draw.rect(self.window, (0, 0, 255), option_rect)
            option_surface_rect = option_surface.get_rect(center=option_rect.center)
            self.window.blit(option_surface, option_surface_rect)

    def display_player_type_selection(self):
        # Prompt to ask if the player is human or computer
        current_player = len(self.players_type) + 1
        if current_player > self.num_players:
            self.transition_to_game = True  # All players have been selected, transition to the game
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

    def handle_click(self, pos):
        if self.selection_phase == "num_players":
            self.handle_num_players_click(pos)
        elif self.selection_phase == "player_type" and not self.transition_to_game:
            self.handle_player_type_click(pos)

    def handle_num_players_click(self, pos):
        for i in range(2, 5):
            option_rect = pygame.Rect(300 + (i - 2) * 100, 250, 50, 50)
            if option_rect.collidepoint(pos):
                self.num_players = i
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
            self.transition_to_game = True

    def start_game(self):
        return self.transition_to_game
