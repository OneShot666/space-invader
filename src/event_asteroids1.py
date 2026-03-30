from src.asteroids1 import Asteroid1
from src.player1 import Player1
import pygame


class AsteroidGroup1:
    def __init__(self, player: Player1):
        self.player = player
        self.wave = 1
        self.frequence = 0
        self.asteroids = pygame.sprite.Group()

    def start_event(self):                                                      # Créer infinité d'astéroides
        self.frequence += 1

        if self.frequence == 15:
            self.asteroids.add(Asteroid1(self.player))
            self.frequence = 0
            print(f"Attention, {len(self.asteroids)} astéroides en vue !")
