"""
This module contains the Button class, which is used to create clickable buttons in the game.
"""
import pygame
from app.config import SCREEN_HEIGHT, SCREEN_WIDTH

BUTTON_WIDTH = 320
BUTTON_HEIGHT = 36
BUTTON_COLOR = (150, 150, 150)
PRESSED_COLOR = (94, 94, 94)


class Button:
    """
    A clickable button.
    """
    def __init__(self, y_offset, text):
        """
        Initialize the button.
        """
        self.rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.clicked = False
        self.color = BUTTON_COLOR
        self.text = text
        self.rect.x = (SCREEN_WIDTH - self.rect.width) / 2
        self.rect.y = (SCREEN_HEIGHT - self.rect.height) / 2 + y_offset

    def draw(self, surface):
        """
        Draw the button on the given surface.
        """
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.rect.collidepoint(mouse_pos):
            surface.fill(PRESSED_COLOR, self.rect)
        else:
            surface.fill(BUTTON_COLOR, self.rect)

        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        surface.blit(text, text_rect)

        return action

    def is_clicked(self):
        """
        Check if the button was clicked.
        """
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
