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
        # Set the pygame window where the menu will be displayed
        self.window = window

        # Set up the font for displaying text in the menu
        self.font = pygame.font.SysFont('Arial', 24)

        # Set up the font for the title of the game
        self.title_font = pygame.font.SysFont('Arial', 40)

        # Initialize the number of players to None as it's not yet selected
        self.num_players = None

        # Initialize an empty list to hold the types of players (e.g., Human, Computer)
        self.players_type = []

        # Initialize the size of the board to None, as it will be selected later
        self.board_size = None

        # Initialize player colors to None, as they will be determined based on game settings
        self.player_colors = None

        # Set the initial phase of the menu to "num_players", where players select the number of players
        self.selection_phase = "num_players"

        # Initialize the flag for transitioning into the game, set to False until game settings are confirmed
        self.transition_to_game = False

        # Initialize wheel spinning to False, used for 4-player mode to determine the order of play
        self.is_wheel_spinning = False

        # Set the initial angle of the spinning wheel to 0 degrees
        self.wheel_angle = 0

        # Set the initial spin speed of the wheel to 0 (no spin at the beginning)
        self.spin_speed = 0

        # Set the center of the wheel to the coordinates (400, 400)
        self.center = (400, 400)

        # Set the radius of the spinning wheel to 200 pixels
        self.radius = 200

        # Initialize the winner of the wheel spin to None, as the wheel has not spun yet
        self.winner = None

        # Initialize an empty list to store the order of players based on the wheel spin
        self.spin_order = []

        # Initialize the user’s choice for the coin toss to None (used in 2-player mode)
        self.user_choice = None

        # Set the coin flipping status to False, indicating that the coin is not currently flipping
        self.coin_flipping = False

        # Initialize the result of the coin toss to None
        self.coin_flip_result = None

        # Create a rectangle for the "Load Game" button with dimensions and position
        self.load_game_button_rect = pygame.Rect(300, 400, 200, 50)

        # Initialize the selected game case to None (used when loading a saved game)
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
        # Fill the window with a background color (light gray).
        self.window.fill((240, 240, 240))

        # Render the game title using the title font and set the color to black.
        title_surface = self.title_font.render("Lines of Action", True, (0, 0, 0))

        # Set the position of the game title to be centered at (400, 100).
        title_rect = title_surface.get_rect(center=(400, 100))

        # Blit (draw) the title text onto the window.
        self.window.blit(title_surface, title_rect)

        # Display the appropriate menu options based on the current selection phase.
        if self.selection_phase == "num_players":
            # If the phase is selecting the number of players, call the corresponding display function.
            self.display_num_players_selection()
        elif self.selection_phase == "player_type":
            # If the phase is selecting the type of players, call the corresponding display function.
            self.display_player_type_selection()
        elif self.selection_phase == "board_size":
            # If the phase is selecting the board size, call the corresponding display function.
            self.display_board_size_selection()
        elif self.selection_phase == "coin_toss" and self.num_players == 2:
            # If it's a 2-player game, display the coin toss phase.
            self.display_coin_toss()
        elif self.selection_phase == "wheel_spin" and self.num_players == 4:
            # If it's a 4-player game, display the wheel spin phase.
            self.display_wheel_spin()
        elif self.selection_phase == "load_game":
            # If the "Load Game" option was selected, display the available load game cases.
            self.display_load_game_cases()

        # Update the window to display the rendered content.
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
        # Render the prompt asking "How many players?" with the font and color black.
        prompt_surface = self.font.render("How many players? (2 or 4)", True, (0, 0, 0))

        # Set the position of the prompt to be centered at (400, 200).
        prompt_rect = prompt_surface.get_rect(center=(400, 200))

        # Blit the prompt text onto the window.
        self.window.blit(prompt_surface, prompt_rect)

        # Loop through the options for number of players (2 and 4).
        for i, num in enumerate([2, 4]):
            # Render the number of players (2 or 4) using the font and color black.
            option_surface = self.font.render(str(num), True, (0, 0, 0))

            # Create a rectangular area for each option at positions 300 and 400.
            option_rect = pygame.Rect(300 + i * 100, 250, 50, 50)

            # Draw the rectangle for each option, with a blue background.
            pygame.draw.rect(self.window, (0, 0, 255), option_rect)

            # Set the text to be centered inside the rectangle.
            option_surface_rect = option_surface.get_rect(center=option_rect.center)

            # Blit the option text (2 or 4) onto the window.
            self.window.blit(option_surface, option_surface_rect)

        # Draw the "Load Game" button rectangle in black.
        pygame.draw.rect(self.window, (0, 0, 0), self.load_game_button_rect)

        # Render the text "Load Game" in white to be displayed on the button.
        load_game_surface = self.font.render("Load Game", True, (255, 255, 255))

        # Set the position of the "Load Game" text to be centered inside the button.
        load_game_surface_rect = load_game_surface.get_rect(center=self.load_game_button_rect.center)

        # Blit the "Load Game" text onto the button.
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
        # Loop through five cases to create buttons for each saved game case.
        for i in range(5):
            # Create a rectangle for the case button, positioning them 60 units apart vertically.
            button_rect = pygame.Rect(300, 200 + i * 60, 200, 50)

            # Draw the rectangle for each case button, with a blue background.
            pygame.draw.rect(self.window, (0, 0, 255), button_rect)

            # Render the case label (e.g., "Case 1", "Case 2") using the font and white color.
            case_surface = self.font.render(f"Case {i + 1}", True, (255, 255, 255))

            # Set the text to be centered inside the button rectangle.
            case_rect = case_surface.get_rect(center=button_rect.center)

            # Blit (draw) the case label onto the button.
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
        # Render the prompt "Select board size:" using the font and black color.
        prompt_surface = self.font.render("Select board size:", True, (0, 0, 0))

        # Set the position of the prompt to be centered at (400, 200).
        prompt_rect = prompt_surface.get_rect(center=(400, 200))

        # Blit the prompt text onto the window.
        self.window.blit(prompt_surface, prompt_rect)

        # Determine the board sizes based on the number of players (12x12 and 16x16 for 4 players, 8x8 for 2 players).
        sizes = [12, 16] if self.num_players == 4 else [8]

        # Loop through the available board sizes to create clickable options.
        for i, size in enumerate(sizes):
            # Render the board size (e.g., "12 x 12", "16 x 16") using the font and black color.
            option_surface = self.font.render(f"{size} x {size}", True, (0, 0, 0))

            # Create a rectangular button for each board size.
            option_rect = pygame.Rect(300 + i * 100, 250, 100, 50)

            # Draw the rectangle for the board size option, with a blue background.
            pygame.draw.rect(self.window, (0, 0, 255), option_rect)

            # Set the text to be centered inside the button rectangle.
            option_surface_rect = option_surface.get_rect(center=option_rect.center)

            # Blit the board size text onto the button.
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
        # Determine the current player based on how many player types have been selected
        current_player = len(self.players_type) + 1

        # If all players have been assigned a type, move to the board size selection phase
        if current_player > self.num_players:
            self.selection_phase = "board_size"
            return

        # Render the prompt asking if the current player is human or computer
        prompt_surface = self.font.render(f"Is Player {current_player} human or computer?", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(400, 200))
        # Display the prompt on the screen
        self.window.blit(prompt_surface, prompt_rect)

        # Define the rectangle areas for the Human and Computer buttons
        human_button_rect = pygame.Rect(250, 250, 150, 50)
        computer_button_rect = pygame.Rect(450, 250, 150, 50)

        # Draw the buttons with green for Human and red for Computer
        pygame.draw.rect(self.window, (0, 255, 0), human_button_rect)
        pygame.draw.rect(self.window, (255, 0, 0), computer_button_rect)

        # Render the text for the Human and Computer buttons
        human_surface = self.font.render("Human", True, (0, 0, 0))
        computer_surface = self.font.render("Computer", True, (0, 0, 0))

        # Display the text on top of the buttons
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
    Reference: Chatgpt
    """

    def display_coin_toss(self):
        # If the user hasn't made a choice, display the heads and tails buttons
        if not self.user_choice:
            # Define the rectangle areas for the Heads and Tails buttons
            heads_button_rect = pygame.Rect(300, 300, 100, 50)
            tails_button_rect = pygame.Rect(450, 300, 100, 50)

            # Draw the buttons with green for Heads and red for Tails
            pygame.draw.rect(self.window, (0, 255, 0), heads_button_rect)
            pygame.draw.rect(self.window, (255, 0, 0), tails_button_rect)

            # Render the text for the Heads and Tails buttons
            heads_surface = self.font.render("Heads", True, (0, 0, 0))
            tails_surface = self.font.render("Tails", True, (0, 0, 0))

            # Display the text on top of the buttons
            self.window.blit(heads_surface, heads_button_rect.move(10, 10))
            self.window.blit(tails_surface, tails_button_rect.move(10, 10))

        # If the coin is currently flipping, simulate the coin toss animation
        elif self.coin_flipping:
            # Randomly pick either "Heads" or "Tails" to simulate the coin flipping
            coin_side = random.choice(["Heads", "Tails"])
            # Display the flipping result (this will update as the coin "flips")
            result_surface = self.font.render(f"Coin is flipping: {coin_side}", True, (0, 0, 0))
            self.window.blit(result_surface, (300, 250))
            pygame.display.update()

            # Delay for a short moment to simulate flipping
            pygame.time.delay(300)

            # Stop flipping if the random condition is met
            if random.random() > 0.8:
                self.coin_flipping = False
                # Randomly decide the final coin toss result
                self.coin_flip_result = random.choice(["Heads", "Tails"])

        # Once the coin flip is done, display the final result
        else:
            # Display the result of the coin toss
            result_text = f"The coin landed on {self.coin_flip_result.upper()}!"
            result_surface = self.font.render(result_text, True, (0, 0, 0))
            self.window.blit(result_surface, (300, 250))

            # Determine who will play as Black and go first based on the coin flip result
            if self.user_choice == self.coin_flip_result:
                player_text = "Player 1 will play as Black and go first."
                self.player_color = (0, 0, 0)  # Player is black
                self.computer_color = (255, 255, 255)  # Computer is white
            else:
                player_text = "Player 2 will play as Black and go first."
                self.player_color = (255, 255, 255)  # Player is white
                self.computer_color = (0, 0, 0)  # Computer is black

            # Display the message stating who plays as Black and goes first
            player_surface = self.font.render(player_text, True, (0, 0, 0))
            self.window.blit(player_surface, (300, 300))

            # Update the display and wait for a moment before transitioning to the game
            pygame.display.update()
            pygame.time.wait(2000)

            # Set the flag to transition into the game after the coin toss
            self.transition_to_game = True

    """
    Function Name: display_wheel_spin
    Purpose: To display and manage the 4-player wheel spin.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Render a spinning wheel and allow players to spin to determine the starting order.
    Reference: Chatgpt
    """

    def display_wheel_spin(self):
        # If the wheel is not spinning, display the "Spin" button
        if not self.is_wheel_spinning:
            # Define the rectangle for the spin button
            spin_button_rect = pygame.Rect(350, 550, 100, 50)
            # Draw the spin button in green
            pygame.draw.rect(self.window, (0, 255, 0), spin_button_rect)
            # Render the text "Spin" for the button
            spin_text = self.font.render("Spin", True, (0, 0, 0))
            # Display the text on top of the button
            self.window.blit(spin_text, spin_button_rect.move(20, 10))
        else:
            # If the wheel is spinning, draw the wheel
            self.draw_wheel()
            # If the spin speed is greater than 0, continue spinning the wheel
            if self.spin_speed > 0:
                # Update the wheel's angle based on the spin speed
                self.wheel_angle += self.spin_speed
                # Gradually decrease the spin speed (simulate friction)
                self.spin_speed *= 0.98
                # Stop the wheel if the spin speed is too low
                if self.spin_speed < 0.1:
                    self.spin_speed = 0
            else:
                # Once the wheel stops spinning, determine the winner
                self.is_wheel_spinning = False
                self.determine_winner()

    """
    Function Name: draw_wheel
    Purpose: To draw the wheel with 4 sections representing the players.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Render a spinning wheel divided into 4 sections, each representing a player.
    Reference: Chatgpt
    """

    def draw_wheel(self):
        # Define the number of sections in the wheel
        num_sections = 4
        # Define the colors for each section
        section_colors = [(200, 200, 200), (150, 150, 150), (100, 100, 100), (50, 50, 50)]
        # Define the labels for each section (Player 1, 2, 3, 4)
        section_labels = ["1", "2", "3", "4"]

        # Loop through each section of the wheel
        for i in range(num_sections):
            # Calculate the starting and ending angles for each section
            start_angle = i * (360 // num_sections)
            end_angle = (i + 1) * (360 // num_sections)
            # Draw the polygon representing the section
            pygame.draw.polygon(self.window, section_colors[i],
                                self.get_wheel_section_points(start_angle, end_angle))

            # Render the label for the section
            text_surface = self.font.render(section_labels[i], True, (0, 0, 0))
            # Calculate the position for the label
            text_rect = text_surface.get_rect(center=self.get_wheel_section_center(start_angle, end_angle))
            # Display the label on the wheel
            self.window.blit(text_surface, text_rect)

        # Draw the arrow indicating the selected section
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
    Reference: Chatgpt
    """

    def get_wheel_section_points(self, start_angle, end_angle):
        # Start the points list with the center of the wheel
        points = [self.center]
        # Loop through the start and end angles of the section
        for angle in (start_angle, end_angle):
            # Calculate the x-coordinate using the cosine of the angle
            x = self.center[0] + self.radius * math.cos(math.radians(angle + self.wheel_angle))
            # Calculate the y-coordinate using the sine of the angle
            y = self.center[1] + self.radius * math.sin(math.radians(angle + self.wheel_angle))
            # Add the calculated point to the points list
            points.append((x, y))
        # Return the points for the section
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
    Reference: Chatgpt
    """

    def get_wheel_section_center(self, start_angle, end_angle):
        # Calculate the midpoint angle between start and end angles
        mid_angle = (start_angle + end_angle) / 2
        # Calculate the x-coordinate of the section center using trigonometry
        x = self.center[0] + self.radius / 1.5 * math.cos(math.radians(mid_angle + self.wheel_angle))
        # Calculate the y-coordinate of the section center using trigonometry
        y = self.center[1] + self.radius / 1.5 * math.sin(math.radians(mid_angle + self.wheel_angle))
        # Return the center point of the wheel section
        return (x, y)

    """
    Function Name: draw_wheel_arrow
    Purpose: To draw an arrow pointing at the current section of the wheel.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Draw a triangular arrow at the top of the wheel, indicating the selected section.
    Reference: Chatgpt
    """

    def draw_wheel_arrow(self):
        # Define the points for the triangular arrow
        arrow_points = [
            (self.center[0] - 10, self.center[1] - self.radius - 10),  # Left point
            (self.center[0] + 10, self.center[1] - self.radius - 10),  # Right point
            (self.center[0], self.center[1] - self.radius)  # Top point
        ]
        # Draw the arrow in red
        pygame.draw.polygon(self.window, (255, 0, 0), arrow_points)

    """
    Function Name: determine_winner
    Purpose: To determine the winner based on the final wheel position.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Use the wheel angle to determine which section the arrow is pointing to.
        2) Assign the winning player and set the colors based on the winner.
    Reference: Chatgpt
    """

    def determine_winner(self):
        # Calculate the section of the wheel that the arrow is pointing to based on the wheel angle
        section = int(self.wheel_angle % 360 // (360 // 4)) + 1
        # Set the winner to the corresponding section number
        self.winner = section

        # Assign player colors based on the winning section
        if self.winner == 1:
            self.player_colors = {1: (0, 0, 0), 2: (255, 255, 255), 3: (255, 0, 0), 4: (0, 255, 0)}
        elif self.winner == 2:
            self.player_colors = {2: (0, 0, 0), 3: (255, 255, 255), 4: (255, 0, 0), 1: (0, 255, 0)}
        elif self.winner == 3:
            self.player_colors = {3: (0, 0, 0), 4: (255, 255, 255), 1: (255, 0, 0), 2: (0, 255, 0)}
        elif self.winner == 4:
            self.player_colors = {4: (0, 0, 0), 1: (255, 255, 255), 2: (255, 0, 0), 3: (0, 255, 0)}

        # Wait for 2 seconds before transitioning to the game
        pygame.time.wait(2000)
        # Set the transition to game flag to True
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
    Reference: Chatgpt
    """

    def handle_click(self, pos):
        # Check which selection phase the menu is in and handle accordingly
        if self.selection_phase == "num_players":
            # Handle clicks for selecting number of players
            self.handle_num_players_click(pos)
        elif self.selection_phase == "player_type" and not self.transition_to_game:
            # Handle clicks for selecting player type
            self.handle_player_type_click(pos)
        elif self.selection_phase == "board_size":
            # Handle clicks for selecting board size
            self.handle_board_size_click(pos)
        elif self.selection_phase == "coin_toss":
            # Handle clicks for the coin toss phase
            self.handle_coin_toss_click(pos)
        elif self.selection_phase == "wheel_spin":
            # Handle clicks for the wheel spin phase
            self.handle_wheel_spin_click(pos)
        elif self.selection_phase == "load_game":
            # Handle clicks for loading a saved game
            self.handle_load_game_click(pos)

        # Check if the "Load Game" button was clicked in the number of players selection phase
        if self.selection_phase == "num_players" and self.load_game_button_rect.collidepoint(pos):
            # Transition to the "Load Game" selection phase
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
    Reference: Chatgpt
    """

    def handle_load_game_click(self, pos):
        # Loop through the 5 available save slots
        for i in range(5):
            # Create a rectangular area for each save slot button
            button_rect = pygame.Rect(300, 200 + i * 60, 200, 50)
            # Check if the mouse click is within the bounds of the button
            if button_rect.collidepoint(pos):
                # Set the selected case to the corresponding save slot number
                self.selected_case = i + 1
                # Transition to the game once a save slot is selected
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
    Reference: Chatgpt
    """

    def handle_wheel_spin_click(self, pos):
        # Define the rectangular area for the "Spin" button
        spin_button_rect = pygame.Rect(350, 550, 100, 50)
        # Check if the mouse click is within the bounds of the spin button
        if spin_button_rect.collidepoint(pos) and not self.is_wheel_spinning:
            # Start spinning the wheel by setting the spin state and speed
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
        # Loop through the available player options (2 and 4 players)
        for i, num in enumerate([2, 4]):
            # Create a rectangular area for each option
            option_rect = pygame.Rect(300 + i * 100, 250, 50, 50)
            # Check if the mouse click is within the bounds of the option
            if option_rect.collidepoint(pos):
                # Set the selected number of players
                self.num_players = num
                # Move to the next phase to select player types
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
        # Define the rectangular areas for "Human" and "Computer" buttons
        human_button_rect = pygame.Rect(250, 250, 150, 50)
        computer_button_rect = pygame.Rect(450, 250, 150, 50)

        # Check if the mouse click is within the "Human" button
        if human_button_rect.collidepoint(pos):
            self.players_type.append("Human")
        # Check if the mouse click is within the "Computer" button
        elif computer_button_rect.collidepoint(pos):
            self.players_type.append("Computer")

        # Once all players have been selected, move to the board size selection phase
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
        # Define available board sizes based on the number of players
        sizes = [12, 16] if self.num_players == 4 else [8, 12, 16]
        # Loop through the available board sizes
        for i, size in enumerate(sizes):
            # Create a rectangular area for each board size option
            option_rect = pygame.Rect(300 + i * 100, 250, 100, 50)
            # Check if the mouse click is within the bounds of the option
            if option_rect.collidepoint(pos):
                # Store the selected board size
                self.board_size = size
                # Move to the next phase (coin toss for 2 players or wheel spin for 4 players)
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
        # If transitioning to the game, return the necessary settings
        if self.transition_to_game:
            # If a saved case was selected, return the loaded game settings
            if self.selected_case:
                return {
                    'num_players': 2,
                    'players_type': ["Human", "Computer"],
                    'board_size': 8,
                    'player_order': None,
                    'player_colors': None,
                    'case': self.selected_case
                }
            # For a new 2-player game, return the relevant settings
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
            # For a new 4-player game, return the relevant settings
            else:
                return {
                    'num_players': self.num_players,
                    'players_type': self.players_type,
                    'player_order': self.spin_order,
                    'player_colors': self.player_colors,
                    'board_size': self.board_size
                }
        # If not transitioning to the game, return None
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
    Reference: Chatgpt
    """

    def handle_coin_toss_click(self, pos):
        # Define the rectangular areas for "Heads" and "Tails" buttons
        heads_button_rect = pygame.Rect(300, 300, 100, 50)
        tails_button_rect = pygame.Rect(450, 300, 100, 50)

        # Check if the mouse click is within the "Heads" button and store the choice
        if heads_button_rect.collidepoint(pos) and not self.user_choice:
            self.user_choice = "Heads"
            self.coin_flipping = True
        # Check if the mouse click is within the "Tails" button and store the choice
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
        # If a saved case was selected, return the loaded game settings
        if self.selected_case:
            return {
                'num_players': 2,
                'players_type': ["Human", "Computer"],
                'board_size': 8,
                'player_order': None,
                'player_colors': None,
                'case': self.selected_case
            }
        # If no saved case was selected, return None
        return None

