"""Represents pause menu class"""
from app.button import Button, BUTTON_HEIGHT
PADDING = 20


class PauseMenu:
    """Pause menu class"""
    def __init__(self):
        """Initialize pause menu class"""
        self.save_and_go_to_main_menu_button = Button(-(BUTTON_HEIGHT + PADDING), "Save and go to main menu")
        self.continue_playing_button = Button(0, "Continue playing")

    def draw(self, surface):
        """Draw pause menu"""
        self.save_and_go_to_main_menu_button.draw(surface)
        self.continue_playing_button.draw(surface)

    def save_and_go_to_main_menu_button_is_clicked(self):
        """Check if button was clicked"""
        return self.save_and_go_to_main_menu_button.is_clicked()

    def continue_playing_button_is_clicked(self):
        """Check if button was clicked"""
        return self.continue_playing_button.is_clicked()
