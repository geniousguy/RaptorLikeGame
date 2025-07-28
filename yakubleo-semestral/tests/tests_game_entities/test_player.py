"""Tests for player class."""

from app.game_entities.player import Player
from app.game_entities.bullet import Bullet


def test_player_creation():
    """Tests creating a Player object."""
    player = Player(100, 100, 30, 30)
    assert player.rect.x == 100
    assert player.rect.y == 100
    assert player.rect.width == 30
    assert player.rect.height == 30
    assert player.color == (255, 0, 0)
    assert player.speed == 7
    assert not player.bullets
    assert player.bullet_damage == 1


def test_player_shoot_no_bullets():
    """Tests shooting a bullet when there are no bullets."""
    player = Player(100, 100, 30, 30)
    number_of_bullets_before = len(player.bullets)

    player.shoot()

    assert len(player.bullets) == number_of_bullets_before + 1
    assert isinstance(player.bullets[0], Bullet)


def test_player_shoot_max_bullets():
    """Tests shooting when at the maximum bullet limit."""
    player = Player(100, 100, 30, 30)
    for _ in range(20):
        player.shoot()

    player.shoot()

    assert len(player.bullets) == 20


def test_player_shoot_bullet_position():
    """Tests the position of the newly created bullet."""
    player = Player(100, 100, 30, 30)
    player.shoot()
    bullet = player.bullets[0]

    assert bullet.rect.x == player.rect.centerx
    assert bullet.rect.y == player.rect.top
