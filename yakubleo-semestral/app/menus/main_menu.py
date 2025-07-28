"""Represents main menu"""
from app.button import Button, BUTTON_HEIGHT
PADDING = 20


class MainMenu:
    """Main menu"""
    def __init__(self):
        """Initialize main menu"""
        self.start_game_button = Button(-(BUTTON_HEIGHT + PADDING), "Start New Game")
        self.load_game_button = Button(0, "Load Previous Game")
        self.exit_button = Button(BUTTON_HEIGHT + PADDING, "Exit")

    def draw(self, surface):
        """Draw main menu"""
        self.start_game_button.draw(surface)
        self.load_game_button.draw(surface)
        self.exit_button.draw(surface)

    def exit_button_is_clicked(self):
        """Check if exit button is clicked"""
        return self.exit_button.is_clicked()

    def start_game_button_is_clicked(self):
        """Check if start game button is clicked"""
        return self.start_game_button.is_clicked()

    def load_game_button_is_clicked(self):
        """Check if load game button is clicked"""
        return self.load_game_button.is_clicked()
