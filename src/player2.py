from rocket2 import *
from vars import *
import pygame


class Player2(pygame.sprite.Sprite):
    def __init__(self, jeu):
        super().__init__()
        self.game = jeu
        self.health = 300
        self.health_max = 300
        self.energy = 0
        self.energy_max = 150
        self.xp = 0
        self.xp_max = 100
        self.attack = 100
        self.speed = 15
        self.regen_energy = 1.5
        self.width = (taille_fenetre[0] * 0.1) // 1
        self.height = (self.width * 0.5) // 1
        self.bar_height = (self.height * 0.1) // 1
        self.image = pygame.image.load('../images/spaceship2.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.width
        self.rect.y = (taille_fenetre[1] * 0.5 - self.height * 0.5) // 1
        self.rockets = pygame.sprite.Group()

    def update_health_bar(self, surface):                                      # Barre de vie
        pygame.draw.rect(surface, (30, 80, 30), [self.rect.x, self.rect.y - 4 * self.bar_height,
                                                 self.health_max / self.health_max * self.width, self.bar_height])
        pygame.draw.rect(surface, (48, 225, 25), [self.rect.x, self.rect.y - 4 * self.bar_height,
                                                  self.health / self.health_max * self.width, self.bar_height])

        if self.health < self.health_max * 0.1:
            print("Attention Commandant, l'armure est gravement touché !")

    def update_energy_bar(self, surface):                                      # Barre d'énergie
        pygame.draw.rect(surface, (0, 95, 245), [self.rect.x, self.rect.y - 3 * self.bar_height,
                                                 self.energy_max / self.energy_max * self.width, self.bar_height])
        pygame.draw.rect(surface, (0, 205, 255), [self.rect.x, self.rect.y - 3 * self.bar_height,
                                                  self.energy / self.energy_max * self.width, self.bar_height])

    def update_xp_bar(self, surface):                                          # Barre d'xp
        pygame.draw.rect(surface, (120, 90, 0), [self.rect.x, self.rect.y - 2 * self.bar_height,
                                                 self.xp_max / self.xp_max * self.width, self.bar_height])
        pygame.draw.rect(surface, (255, 215, 0), [self.rect.x, self.rect.y - 2 * self.bar_height,
                                                  self.xp / self.xp_max * self.width, self.bar_height])

    def take_damage(self, amount):                                             # Prend des dégâts
        if self.health - amount > amount:
            self.health -= amount
            print(f"Dégâts pris ! ({amount})")
        else:
            self.game.game_over()

    def take_energy(self, amount):                                             # Récupère de l'énergie
        if self.energy + amount <= self.energy_max:
            self.energy += amount
        else:
            self.energy = self.energy_max
            print("Energie max !")

    def take_experience(self, amount):                                         # Gagne de l'xp
        self.xp += amount

        while self.xp > self.xp_max:
            self.level_up()

    def level_up(self):
        self.xp -= self.xp_max
        self.xp_max += 50
        self.health = self.health_max
        self.energy = self.energy_max
        self.game.rocket.attack += 1
        print("Level Up !")

    def move_up(self):                                                         # Déplacements
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):                                                           # Attaque
        self.rockets.add(PlasmaShooter2(self))
