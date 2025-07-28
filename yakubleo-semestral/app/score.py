"""
Represents score calculations.
"""
import pygame
from app.config import SCREEN_HEIGHT, SCREEN_WIDTH


class Score:
    """Score"""
    def __init__(self):
        """Initialize score."""
        self.score = 0

    def increment(self):
        """Increment score."""
        self.score += 1

    def draw(self, surface):
        """Draw score."""
        font = pygame.font.Font(None, 32)
        text_surface = font.render("Score: " + str(self.score), True, (255, 255, 255))
        surface.blit(text_surface, (SCREEN_WIDTH - text_surface.get_width() - 10, SCREEN_HEIGHT - 30))
