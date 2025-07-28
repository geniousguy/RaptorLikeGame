"""Tests for rocket class."""
from app.powerups.rocket import Rocket
from app.game_entities.enemy import Enemy


def test_rocket_creation():
    """Tests creating a Rocket object with a target enemy."""
    enemy = Enemy(200, 100, "basic")
    rocket_with_enemy = Rocket(100, 150, enemy)
    assert rocket_with_enemy.target_enemy is not None
    assert rocket_with_enemy.rect.x == 100
    assert rocket_with_enemy.rect.y == 150
    assert rocket_with_enemy.speed == 20


def test_rocket_update_with_enemy():
    """Tests updating Rocket with a target enemy."""

    enemy = Enemy(200, 100, "basic")
    rocket_with_enemy = Rocket(100, 150, enemy)

    initial_x = rocket_with_enemy.rect.x
    initial_y = rocket_with_enemy.rect.y

    rocket_with_enemy.target_enemy = enemy

    rocket_with_enemy.update()

    assert rocket_with_enemy.rect.x != initial_x
    assert rocket_with_enemy.rect.y != initial_y
    assert rocket_with_enemy.rect.x < 200
    assert rocket_with_enemy.rect.y < 150
