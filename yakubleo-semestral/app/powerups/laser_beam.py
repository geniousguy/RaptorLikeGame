"""Laser beam class"""
import pygame


class LaserBeam:
    """Laser beam class"""
    def __init__(self, x, y, width, height):
        """Initialize laser beam class"""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (128, 0, 128)  # Purple color

    def draw(self, screen):
        """Draw laser beam on screen"""
        pygame.draw.rect(screen, self.color, self.rect)

    def collides(self, rect):
        """Check if laser beam collides with rect"""
        return rect.colliderect(self.rect)
