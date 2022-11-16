from asteroids1 import *
import pygame


class AsteroidGroup1:
    def __init__(self, game):
        self.game = game
        self.vague = 1
        self.variable = 0
        self.asteroids = pygame.sprite.Group()

    def start_event(self):                                                      # Créer infinité d'astéroides
        self.variable += 1

        if self.variable == 15:
            self.asteroids.add(Asteroid1(self))
            self.variable = 0
            print(f"Attention, {len(self.asteroids)} astéroides en vue !")
