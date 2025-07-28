"""Class that represents a player entity."""
import pygame
from app.game_entities.bullet import Bullet
from app.config import SCREEN_HEIGHT, SCREEN_WIDTH


class Player:
    """Represents a player entity."""
    def __init__(self, x, y, width, height):
        """Initialize a player entity."""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.speed = 7
        self.bullets = []
        self.bullet_damage = 1

    def move(self):
        """Move the player based on key pressed"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        """Shoots bullets"""
        if len(self.bullets) < 20:
            bullet_x = self.rect.centerx
            bullet_y = self.rect.top
            new_bullet = Bullet(bullet_x, bullet_y, self)
            self.bullets.append(new_bullet)

    def draw(self, screen):
        """Draw the player on the screen"""
        pygame.draw.rect(screen, self.color, self.rect)

        for bullet in self.bullets:
            bullet.draw(screen)
