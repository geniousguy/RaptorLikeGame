"""
Tests for button class.
"""
import pygame
from app.button import Button, BUTTON_HEIGHT, BUTTON_WIDTH
from app.config import SCREEN_WIDTH, SCREEN_HEIGHT


def test_button_creation():
    """Tests creating a Button object."""
    button = Button(100, "Test Button")
    assert button.rect.width == BUTTON_WIDTH
    assert button.rect.height == BUTTON_HEIGHT
    assert button.text == "Test Button"
    button.rect.x = (SCREEN_WIDTH - button.rect.width) / 2
    button.rect.y = (SCREEN_HEIGHT - button.rect.height) / 2 + 100


def test_button_not_clicked():
    """Tests if the Button is not clicked."""
    pygame.init()
    button = Button(100, "Test Button")

    assert not button.is_clicked()
    pygame.quit()
