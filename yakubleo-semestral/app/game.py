"""
Game module. Handles all the game logic.
"""
import random
import os
import pickle
import time
import pygame
from app.game_entities.player import Player
from app.powerups.laser_beam import LaserBeam
from app.powerups.powerup import Powerup
from app.powerups.rocket import Rocket
from app.config import SCREEN_WIDTH, SCREEN_HEIGHT
from app.menus.main_menu import MainMenu
from app.menus.pause_menu import PauseMenu
from app.menus.game_over_menu import GameOverMenu
from app.game_entities.enemy import Enemy
from app.score import Score


class Game:
    """
    A game instance.
    """
    def _reset_game(self):
        """
        Reset the game to its initial state.
        """
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, 50, 50)
        self.is_main_menu = True
        self.main_menu = MainMenu()
        self.exit_game = False
        self.is_paused_menu = False
        self.paused_menu = PauseMenu()
        self.game_is_running = False
        self.game_over_menu = GameOverMenu()
        self.is_game_over_menu = False
        self.enemies = []
        self.score = Score()
        self.powerups = []
        self.speed_boost_start_time = None
        self.bullet_damage_boost_start_time = None
        self.laser_start_time = None
        self.laser_beam = None
        self.rockets = []

    def __init__(self):
        """
        Initialize the game instance.
        """
        pygame.init()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, 50, 50)
        self.is_main_menu = True
        self.main_menu = MainMenu()
        self.exit_game = False
        self.is_paused_menu = False
        self.paused_menu = PauseMenu()
        self.game_is_running = False
        self.game_over_menu = GameOverMenu()
        self.is_game_over_menu = False
        self.enemies = []
        self.score = Score()
        self.powerups = []
        self.speed_boost_start_time = None
        self.bullet_damage_boost_start_time = None
        self.laser_start_time = None
        self.laser_beam = None
        self.rockets = []

    def _handle_events(self):
        """
        Handle events such as key presses and mouse clicks.
        """
        for event in pygame.event.get():
            space_pressed = event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
            left_mouse_button_pressed = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            shoot = space_pressed or left_mouse_button_pressed
            if event.type == pygame.QUIT:
                self.exit_game = True
                return False
            if shoot:
                self.player.shoot()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game_is_running = False
                self.is_paused_menu = True
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                self.is_game_over_menu = True
                self.game_is_running = False
                return False

        return True

    # Movement helpers
    def _move_player(self):
        """
        Move the player based on user input.
        """
        self.player.move()

    def _move_enemies(self):
        """
        Move the enemies based on their AI.
        """
        for enemy in self.enemies:
            enemy.move()
            enemy.dodge_bullet(self.player.bullets)

    def _move_rockets(self):
        """
        Move the rockets based on their targets.
        """
        for rocket in self.rockets:
            rocket.update()
            rocket.draw(self.screen)
            if rocket.target_enemy is None:
                self.rockets.remove(rocket)

    def _update_powerups(self):
        """
        Update the powerups and check for collisions with the player.
        """
        for i, powerup in enumerate(self.powerups):
            powerup.update()
            if powerup.rect.colliderect(self.player.rect):
                if powerup.type == "speed":
                    self._activate_speed_boost()
                elif powerup.type == "bullet_damage":
                    self.activate_bullet_damage_boost()
                elif powerup.type == "laser":
                    self.activate_laser()
                elif powerup.type == "rocket":
                    self.activate_rocket()
                self.powerups.pop(i)
                break
        if (self.speed_boost_start_time is not None
                and time.time() - self.speed_boost_start_time > 5):
            self.deactivate_speed_boost()
        if (self.bullet_damage_boost_start_time is not None
                and time.time() - self.bullet_damage_boost_start_time > 5):
            self.deactivate_bullet_damage_boost()
        if (self.laser_start_time is not None
                and time.time() - self.laser_start_time > 5):
            self.deactivate_laser()

    # Activation and deactivation of powerups
    def _activate_speed_boost(self):
        """
        Activate the speed boost powerup.
        """
        if self.speed_boost_start_time is not None:
            return
        self.player.speed *= 2
        self.speed_boost_start_time = time.time()

    def deactivate_speed_boost(self):
        """
        Deactivate the speed boost powerup, resetting the player's speed to its original value.
        """
        self.player.speed /= 2
        self.speed_boost_start_time = None

    def activate_bullet_damage_boost(self):
        """
        Activate the bullet damage boost powerup, increasing the player's bullet damage.
        """
        if self.bullet_damage_boost_start_time is not None:
            return
        self.player.bullet_damage *= 2
        self.bullet_damage_boost_start_time = time.time()

    def deactivate_bullet_damage_boost(self):
        """
        Deactivate the bullet damage boost powerup, resetting the player's bullet damage to its original value.
        """
        self.player.bullet_damage /= 2
        self.bullet_damage_boost_start_time = None

    def activate_laser(self):
        """
        Activate the laser powerup, creating a laser beam that damages enemies.
        """
        self.laser_beam = LaserBeam(self.player.rect.centerx, 0, 2, self.player.rect.top)
        self.laser_start_time = time.time()

    def deactivate_laser(self):
        """
        Deactivate the laser powerup, removing the laser beam.
        """
        self.laser_start_time = None
        self.laser_beam = None

    def activate_rocket(self):
        """
        Activate the rocket powerup, launching a rocket that targets the closest enemy.
        """
        if len(self.enemies) > 0:
            closest_enemy = (
                min(self.enemies,
                    key=lambda enemy: abs(enemy.rect.centerx - self.player.rect.centerx)))
            self.rockets.append(
                Rocket(self.player.rect.centerx, self.player.rect.top, closest_enemy))

    # Spawn functions
    def spawn_enemies(self, start_time):
        """
        Spawn new enemies at a rate based on the game's difficulty level.
        """
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > 1 and len(self.enemies) < 10:
            if random.random() < 0.2:
                self.enemies.append(Enemy(enemy_type="evading"))
            else:
                self.enemies.append(Enemy())
            return current_time
        return start_time

    def spawn_powerups(self, x, y):
        """
        Spawn a random powerup at the given coordinates.
        """
        # if random.random() < 0.5:
        powerup_type = random.choice(["speed", "bullet_damage", "laser", "rocket"])
        if powerup_type == "speed":
            self.powerups.append(Powerup("speed", x, y, (0, 255, 0)))
        elif powerup_type == "bullet_damage":
            self.powerups.append(Powerup("bullet_damage", x, y, (255, 255, 0)))
        elif powerup_type == "laser":
            self.powerups.append(Powerup("laser", x, y, (128, 0, 128)))
        elif powerup_type == "rocket":
            self.powerups.append(Powerup("rocket", x, y, (255, 0, 0)))

    # Draw function
    def draw_screen(self):
        """
        Draw the game screen, including the player, enemies, powerups, and score.
        """
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.score.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        if self.laser_beam is not None:
            self.laser_beam.rect.x = self.player.rect.centerx
            self.laser_beam.rect.height = self.player.rect.top
            self.laser_beam.draw(self.screen)
        for rocket in self.rockets:
            rocket.draw(self.screen)

    # Collision handlers
    def handle_bullet_collision(self):
        """
        Handle collisions between bullets and enemies. If a collision occurs, the bullet is removed,
         the enemy's health is reduced, and if the enemy's health reaches 0, it is removed and a powerup is spawned.
        """
        for i, bullet in enumerate(self.player.bullets):
            for j, enemy in enumerate(self.enemies):
                if enemy.rect.colliderect(bullet.rect):
                    self.player.bullets.pop(i)
                    enemy.hp -= self.player.bullet_damage
                    if enemy.hp <= 0:
                        self.spawn_powerups(enemy.rect.x, enemy.rect.y)
                        self.remove_enemy_from_rockets_target(enemy)
                        self.enemies.pop(j)
                        self.score.increment()
                    break

    def handle_laser_collision(self):
        """
        Handle collisions between the laser beam and enemies. If a collision occurs, the enemy's health is reduced,
         and if the enemy's health reaches 0, it is removed and a powerup is spawned.
        """
        if self.laser_beam is None:
            return
        for j, enemy in enumerate(self.enemies):
            if enemy.rect.colliderect(self.laser_beam.rect):
                enemy.hp -= 1
                if enemy.hp <= 0:
                    self.spawn_powerups(enemy.rect.x, enemy.rect.y)
                    self.remove_enemy_from_rockets_target(enemy)
                    self.enemies.pop(j)
                self.score.increment()
                break

    def remove_enemy_from_rockets_target(self, enemy: Enemy):
        """
        Remove the given enemy from the target list of all rockets.
        """
        for rocket in self.rockets:
            if rocket.target_enemy is enemy:
                rocket.target_enemy = None

    def handle_rocket_collision(self):
        """
        Handle collisions between rockets and enemies.

        This method checks for collisions between rockets and enemies, and if a collision is detected,
        it removes the enemy from the game, removes the rocket from the game, increments the score,
        and spawns power-ups.
        """
        for i, rocket in enumerate(self.rockets):
            for j, enemy in enumerate(self.enemies):
                if enemy.rect.colliderect(rocket.rect):
                    self.remove_enemy_from_rockets_target(enemy)
                    self.enemies.pop(j)
                    self.rockets.pop(i)
                    enemy.hp = 0
                    self.spawn_powerups(enemy.rect.x, enemy.rect.y)
                    self.score.increment()
                    break

    def game_over_condition_check(self):
        """
        Check if an enemy has reached the bottom of the screen.
        """
        for enemy in self.enemies:
            if enemy.rect.bottom >= SCREEN_HEIGHT:
                return True
        return False

    def run_game(self):
        """
        Runs the game itself.
        """
        running = True
        start_time = time.time()
        while running:
            running = self._handle_events()
            self._move_player()
            self._move_enemies()
            self._move_rockets()
            self.draw_screen()
            self._update_powerups()
            self.handle_bullet_collision()
            self.handle_laser_collision()
            self.handle_rocket_collision()
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            start_time = self.spawn_enemies(start_time)
            if self.game_over_condition_check():
                self.game_is_running = False
                self.is_game_over_menu = True
                running = False

    def run(self):
        """
        Encapsulates menus and game in the same function.
        """
        while not self.exit_game:
            if self.is_main_menu:
                self.run_main_menu()
            if self.game_is_running:
                self.run_game()
            if self.is_paused_menu:
                self.run_pause_menu()
            if self.is_game_over_menu:
                self.run_game_over_menu()
        pygame.quit()

    # Loading/saving functions
    def _save_game(self):
        """
        Saves the current game state.
        """
        game_state = {
            "player": self.player,
            "enemies": self.enemies,
            "powerups": self.powerups,
            "score": self.score,
            "speed_boost_start_time": self.speed_boost_start_time,
            "bullet_damage_boost_start_time": self.bullet_damage_boost_start_time,
            "laser_start_time": self.laser_start_time,
            "laser_beam": self.laser_beam,
            "rockets": self.rockets
        }
        with open("game_state.pkl", "wb") as f:
            pickle.dump(game_state, f)

    def load_game(self):
        """
        Loads the game state from the pickle file created in save_game.
        """
        try:
            with open("game_state.pkl", "rb") as f:
                game_state = pickle.load(f)
            self.player = game_state["player"]
            self.enemies = game_state["enemies"]
            self.powerups = game_state["powerups"]
            self.score = game_state["score"]
            self.speed_boost_start_time = game_state["speed_boost_start_time"]
            self.bullet_damage_boost_start_time = game_state["bullet_damage_boost_start_time"]
            self.laser_start_time = game_state["laser_start_time"]
            self.laser_beam = game_state["laser_beam"]
            self.rockets = game_state["rockets"]
        except FileNotFoundError:
            print("No saved game found.")

    # Menu functions
    def run_main_menu(self):
        """Runs the main menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.main_menu.exit_button_is_clicked():
                self.exit_game = True
            if self.main_menu.start_game_button_is_clicked():
                self.is_main_menu = False
                self.game_is_running = True
            if self.main_menu.load_game_button_is_clicked():
                file_path = "game_state.pkl"
                if not os.path.exists(file_path):
                    break
                self.load_game()
                self.is_main_menu = False
                self.game_is_running = True

        self.screen.fill((0, 0, 0))
        self.main_menu.draw(self.screen)
        pygame.display.flip()

    def run_pause_menu(self):
        """Runs the pause menu."""
        for event in pygame.event.get():
            if self.paused_menu.continue_playing_button_is_clicked():
                self.is_paused_menu = False
                self.game_is_running = True
            if event.type == pygame.QUIT:
                self.exit_game = True
            if self.paused_menu.save_and_go_to_main_menu_button_is_clicked():
                self._save_game()
                self._reset_game()
                self.is_paused_menu = False
                self.is_main_menu = True

        self.paused_menu.draw(self.screen)
        pygame.display.flip()

    def run_game_over_menu(self):
        """Runs the game over menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game = True
            if self.game_over_menu.go_to_main_menu_button_is_clicked():
                self._reset_game()
                self.is_game_over_menu = False
                self.is_main_menu = True
        self.game_over_menu.draw(self.screen)
        pygame.display.flip()
