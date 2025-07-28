"""Test enemy class"""
from app.game_entities.enemy import Enemy, ENEMY_HEIGHT, ENEMY_WIDTH, SPEED, MAX_HP, BASIC_COLOR, TYPE, EVADING_COLOR
from app.config import SCREEN_WIDTH


def test_enemy_creation():
    """Tests creating an Enemy object with default arguments."""
    enemy = Enemy()
    assert enemy.rect.width == ENEMY_WIDTH
    assert enemy.rect.height == ENEMY_HEIGHT
    assert enemy.speed == SPEED
    assert enemy.hp == MAX_HP
    assert enemy.type == TYPE
    assert enemy.color == BASIC_COLOR


def test_enemy_creation_with_type():
    """Tests creating an Enemy object with a specific type."""
    enemy = Enemy(enemy_type="evading")
    assert enemy.color == EVADING_COLOR


def test_enemy_move():
    """Tests moving the Enemy down the screen."""
    enemy = Enemy()
    initial_y = enemy.rect.y

    enemy.move()

    assert enemy.rect.y > initial_y


def test_enemy_reset_position():
    """Tests resetting the Enemy's position."""
    enemy = Enemy()
    enemy.rect.x = 100
    enemy.rect.y = 100

    enemy.reset_position()

    assert 0 <= enemy.rect.x < SCREEN_WIDTH - enemy.rect.width
    assert enemy.rect.y == 0
