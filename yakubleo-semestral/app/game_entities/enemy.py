"""Class for enemy entity"""
import random
import pygame
from app.config import SCREEN_WIDTH  # , SCREEN_HEIGHT
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
SPEED = 3
MAX_HP = 2

BASIC_COLOR = (200, 200, 200)
EVADING_COLOR = (34, 77, 44)
TYPE = "basic"


class Enemy:
    """Enemy entity"""
    def __init__(self, x=0, y=0, enemy_type=TYPE):
        """Initialize enemy"""
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.reset_position()
        self.speed = SPEED
        self.hp = MAX_HP
        self.type = enemy_type
        self.color = BASIC_COLOR if enemy_type == "basic" else EVADING_COLOR
        self.dodge_radius = ENEMY_HEIGHT

    def move(self):
        """Move enemy"""
        self.rect.y += self.speed

        # if self.rect.bottom > SCREEN_HEIGHT:
        #     self.reset_position()

    def draw(self, screen):
        """Draw enemy and its hp"""
        font = pygame.font.Font(None, 20)
        hp_text = font.render("HP: " + str(self.hp), True, (255, 255, 255))
        offset_x, offset_y = -15, -15
        text_pos = (self.rect.centerx + offset_x, self.rect.top + offset_y)
        text_rect = pygame.Rect(text_pos, hp_text.get_size())
        screen.blit(hp_text, text_rect)
        pygame.draw.rect(screen, self.color, self.rect)

    def reset_position(self):
        """Reset enemy position"""
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0

    def move_left(self):
        """Dodging helper, teleport left"""
        self.rect.x -= self.rect.width

    def move_right(self):
        """Dodging helper, teleport right"""
        self.rect.x += self.rect.width

    def will_collide_with_bullet(self, bullet):
        """Dodging helper, check if a bullet is close enough"""
        distance_y = bullet.rect.centery - self.rect.centery
        bullet_is_below = bullet.rect.left > self.rect.left and bullet.rect.right < self.rect.right
        return distance_y <= self.dodge_radius and bullet_is_below

    def dodge_bullet(self, bullets):
        """Dodge if a bullet is close"""
        if self.type == "basic":
            return
        for bullet in bullets:
            if self.will_collide_with_bullet(bullet):
                if bullet.rect.centerx < self.rect.centerx:
                    self.move_left()
                else:
                    self.move_right()
                break
