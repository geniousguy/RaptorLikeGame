"""Test powerup class."""

from app.powerups.powerup import Powerup


def test_powerup_creation():
    """Tests creating a Powerup object."""
    powerup = Powerup("laser", 50, 100, (0, 255, 0))

    assert powerup.type == "laser"
    assert powerup.rect.x == 50
    assert powerup.rect.y == 100
    assert powerup.rect.width == 20
    assert powerup.rect.height == 20
    assert powerup.color == (0, 255, 0)


def test_powerup_update_below_screen():
    """Tests powerup movement when below screen height."""
    powerup = Powerup("laser", 10, 20, (255, 0, 0))
    initial_y = powerup.rect.y

    powerup.update()

    assert powerup.rect.y == initial_y + 10
