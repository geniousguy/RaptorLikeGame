"""Test the Bullet class."""
import pygame
from app.game_entities.bullet import Bullet


def test_bullet_creation():
    """Tests creating a Bullet object."""
    bullet = Bullet(10, 20, None)
    assert bullet.rect.x == 10
    assert bullet.rect.y == 20
    assert bullet.color == (255, 255, 255)
    assert bullet.speed == 10


def test_bullet_draw_and_move():
    """Tests drawing and moving the Bullet."""
    mock_screen = pygame.Surface((100, 100))
    bullet = Bullet(10, 20, None)

    bullet.draw(mock_screen)

    assert bullet.rect.x == 10
    assert bullet.rect.y == 10


def test_bullet_remove_from_list():
    """Tests removing the Bullet from a list."""
    bullets = [Bullet(1, 1, None), Bullet(2, 2, None)]
    bullet_to_remove = bullets[0]

    bullet_to_remove.remove_bullet(bullets)

    assert len(bullets) == 1
    assert bullets[0].rect.x == 2
    assert bullets[0].rect.y == 2
