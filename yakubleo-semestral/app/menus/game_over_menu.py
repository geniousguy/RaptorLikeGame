"""Represents game over menu class."""
import pygame
from app.button import Button
PADDING = 70


class GameOverMenu:
    """Represents game over menu"""
    def __init__(self):
        """Initialize game over menu."""
        self.go_to_main_menu_button = Button(0, "Go to main menu")
        self.game_over_font = pygame.font.Font(None, 150)

    def draw(self, surface):
        """Draw game over menu."""
        game_over_text = self.game_over_font.render("Game Over", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(surface.get_width() // 2, self.go_to_main_menu_button.rect.y - PADDING))
        surface.blit(game_over_text, text_rect)

        self.go_to_main_menu_button.draw(surface)

    def go_to_main_menu_button_is_clicked(self):
        """Clicked when game over menu button is clicked."""
        return self.go_to_main_menu_button.is_clicked()
