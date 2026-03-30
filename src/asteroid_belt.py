from src.asteroids import Asteroid
from src.vars import ASTEROID1_NAME
from src.player import Player
import pygame


class AsteroidBelt:
    def __init__(self, screen_size: tuple, player: Player):
        self.screen_size = screen_size
        self.player = player
        # Asteroids manager data
        self.wave = 1
        self.countdown = 0
        self.frequence = 30
        self.asteroid_image = pygame.image.load(ASTEROID1_NAME).convert_alpha()
        self.Asteroids = pygame.sprite.Group()

    def start_event(self):                                                      # Create infinite amount of asteroids
        self.countdown += 1

        if self.countdown == self.frequence:
            self.Asteroids.add(Asteroid(self.screen_size, self.player, self.asteroid_image))
            self.countdown = 0
            print(f"Attention, {len(self.Asteroids)} astéroides en vue !")
