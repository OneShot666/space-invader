from variable import *
import pygame


class PlasmaShooter1(pygame.sprite.Sprite):
    def __init__(self, joueur):
        super().__init__()
        self.attack = 10
        self.speed = 15
        self.cost = 5
        self.player = joueur
        self.image = pygame.image.load(f"{filename_images}/rocket1.png")
        self.width = self.player.width * 0.2
        self.image = pygame.transform.scale(self.image, (self.width, (self.width * 1/3) // 1))
        self.taille = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x + self.player.width
        self.rect.y = (self.player.rect.y + self.player.height * 0.5) // 1

    def move(self):                                                            # Fais bouger la rocket + gère le de-spawn
        self.rect.x += self.speed

        for asteroid in self.player.game.check_collision(self, self.player.game.asteroid_group.asteroids):
            self.auto_destruction()
            asteroid.take_damage(self.attack)

        if self.rect.x > taille_fenetre[0]:
            self.auto_destruction()

    def auto_destruction(self):                                                # Se détruis
        self.player.rockets.remove(self)
