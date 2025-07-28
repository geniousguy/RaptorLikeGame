"""Tests for laser_beam class."""
import pygame
from app.powerups.laser_beam import LaserBeam


def test_laser_beam_creation():
    """Tests creating a LaserBeam object."""
    laser_beam = LaserBeam(10, 20, 5, 10)

    assert laser_beam.rect.x == 10
    assert laser_beam.rect.y == 20
    assert laser_beam.rect.width == 5
    assert laser_beam.rect.height == 10
    assert laser_beam.color == (128, 0, 128)


def test_laser_beam_collides():
    """Tests laser beam collision detection."""
    laser_beam = LaserBeam(10, 20, 5, 10)

    colliding_rect = pygame.Rect(10, 20, 50, 10)
    non_colliding_rect = pygame.Rect(100, 100, 2, 2)

    assert laser_beam.collides(colliding_rect)
    assert not laser_beam.collides(non_colliding_rect)
