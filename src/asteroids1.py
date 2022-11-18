# import pygame
import random
from vars import *


class Asteroid1(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.random = random.uniform(0.5, 2.5)
        self.health = (self.random * 100) // 1
        self.health_max = (self.random * 100) // 1
        self.attack = self.random * 20 // 1
        self.speed = random.uniform(1, 5)
        self.xp = (self.health_max / 10) // 1
        self.width = (self.random * taille_fenetre[0] * 0.05) // 1
        self.height = (self.width * 1) // 1
        self.ordonne = random.randint(0, 100)
        self.bar_height = 5
        self.image = pygame.image.load(f'{filename_images}/asteroids1.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.taille = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = taille_fenetre[0] + random.randint(1, 5) * self.taille[1]
        self.rect.y = taille_fenetre[1] / 100 * self.ordonne

    def update_health_bar(self, surface):                                      # Barre de vie
        pygame.draw.rect(surface, (30, 80, 30), [self.rect.x, self.rect.y - 2 * self.bar_height,
                                                 self.health_max / self.health_max * self.width, self.bar_height])
        pygame.draw.rect(surface, (48, 225, 25), [self.rect.x, self.rect.y - 2 * self.bar_height,
                                                  self.health / self.health_max * self.width, self.bar_height])

    def take_damage(self, amount):                                             # Prend des dégâts
        if self.health - amount > amount:
            self.health -= amount
        else:                                                                  # Meurt (joueur gagne xp + score)
            self.auto_destruction()
            self.player.game.joueur.take_experience(self.xp)
            self.player.game.add_score(self.xp)
            print(f"Astéroide détruit ! (+{self.xp}xp)")
            print(f"Score : {self.player.game.score}")

    def chute(self):                                                           # Gère collisions + groupe astéroides + dégâts
        self.rect.x -= self.speed

        if self.player.game.check_collision(self, self.player.game.players):
            self.player.game.sound_manager.play("explosion")
            self.auto_destruction()
            self.player.game.joueur.take_damage(self.attack)
            print(f"Vaisseau touché ! (-{self.attack}pv)")

        if self.rect.x + self.taille[0] < 0:                                   # Sort par la gauche
            self.auto_destruction()
            self.player.game.joueur.take_experience(1)
            print("Ouf, on a évité un astéroide !")

    def auto_destruction(self):                                                # Se détruis
        self.player.game.asteroid_group.asteroids.remove(self)
