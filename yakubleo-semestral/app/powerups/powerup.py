"""Represents powerup"""
import pygame
from app.config import SCREEN_HEIGHT


class Powerup:
    """Represents a powerup"""
    def __init__(self, powerup_type, x, y, color):
        """Initialize the powerup"""
        self.type = powerup_type
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color

    def draw(self, screen):
        """Draw the powerup"""
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        """Move the powerup until hits the surface"""
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += 10
