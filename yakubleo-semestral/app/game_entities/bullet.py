"""Class for Bullet."""
import pygame


class Bullet:
    """Represents a Bullet."""
    def __init__(self, x, y, player):
        """Initialize Bullet."""
        self.rect = pygame.Rect(x, y, 5, 10)
        self.color = (255, 255, 255)
        self.speed = 10
        self.player = player

    def draw(self, screen):
        """Draw Bullet."""
        pygame.draw.rect(screen, self.color, self.rect)

        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.remove_bullet(self.player.bullets)

    def remove_bullet(self, bullets):
        """Remove Bullet."""
        bullets.remove(self)

    def collision_happened(self, other_rect):
        """Check if Bullet collides with other rectangle"""
        return self.rect.colliderect(other_rect)
