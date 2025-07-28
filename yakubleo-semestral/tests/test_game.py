"""Tests for Game class"""
from app.game import Game
from app.game_entities.enemy import Enemy
from app.config import SCREEN_HEIGHT
from app.powerups.powerup import Powerup
from app.powerups.rocket import Rocket
from app.powerups.laser_beam import LaserBeam


def test_game_initialization():
    """Test if the Game initializes properly"""
    game = Game()
    assert game.player is not None
    assert game.is_main_menu is True
    assert game.score.score == 0


def test_game_over_condition():
    """Test if the game is over if an enemy hits the bottom of the screen"""
    game = Game()
    enemy = Enemy(0, 0, "basic")
    game.enemies.append(enemy)
    enemy.rect.bottom = SCREEN_HEIGHT
    assert game.game_over_condition_check() is True


def test_powerup_collision():
    """Test if player takes a powerup"""
    game = Game()
    powerup = Powerup("speed", game.player.rect.x, game.player.rect.y, (255, 0, 0))
    game.powerups.append(powerup)

    game._update_powerups()

    assert len(game.powerups) == 0


def test_handle_rocket_collision():
    """
    Test if rockets kill enemies
    """
    game = Game()
    enemy = Enemy(10, 10, "basic")
    game.enemies.append(enemy)
    rocket = Rocket(enemy.rect.x, enemy.rect.y, enemy)
    game.rockets.append(rocket)

    # if rocket.rect.colliderect(enemy.rect):
    #     print("Collided")
    # else:
    #     print("Not Collided")

    game.handle_rocket_collision()

    assert len(game.rockets) == 0


def test_handle_laser_collision():
    """Test if laser damages enemies"""
    game = Game()
    enemy = Enemy(game.player.rect.left, 20, "basic")
    game.enemies.append(enemy)
    game.laser_beam = LaserBeam(enemy.rect.x, 0, 2, game.player.rect.top)
    initial_enemy_hp = enemy.hp
    game.handle_laser_collision()
    assert enemy.hp < initial_enemy_hp
