from src.asteroids import Asteroid
from src.player import Player
import pygame


class AsteroidBelt:
    def __init__(self, screen_size: tuple, player: Player, config: dict, ast_config: dict):
        self.screen_size =  screen_size
        self.player =       player
        self.config =       config
        self.ast_config =   ast_config
        # Asteroids manager data
        self.countdown = 0
        self.frequence =    config["density"]
        self.max_quantity = config["max_size"]
        self.asteroid_image = pygame.image.load(ast_config["img"]).convert_alpha()
        self.Asteroids = pygame.sprite.Group()

    def start_event(self):                                                      # Create infinite amount of asteroids
        self.countdown += 1

        if self.countdown == self.frequence and len(self.Asteroids) < self.max_quantity:
            self.Asteroids.add(Asteroid(self.screen_size, self.player, self.asteroid_image,
                self.ast_config, self.config["chaos"]))
            self.countdown = 0

    def draw(self, screen, offset=(0, 0)):
        for asteroid in self.Asteroids:
            screen.blit(asteroid.image, (asteroid.rect.x + offset[0], asteroid.rect.y + offset[1]))
