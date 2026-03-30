from src.vars import *
import pygame


class PlasmaShooter(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.attack = 10
        self.speed = 15
        self.cost = 5
        self.player = player
        self.image = pygame.image.load(BULLET_NAME)
        self.width = self.player.width * 0.2
        self.image = pygame.transform.scale(self.image, (self.width, (self.width * 1/3) // 1))
        self.taille = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x + self.player.width
        self.rect.y = (self.player.rect.y + self.player.height * 0.5) // 1

    def move(self):                                                             # Move rocket + deal dispawn
        self.rect.x += self.speed

        for asteroid in self.player.game.check_collision(self, self.player.game.asteroid_group.asteroids):
            self.player.game.sound_manager.play_sound("explosion")
            self.auto_destruction()
            asteroid.take_damage(self.attack)

        if self.rect.x > self.player.game.screen_size[0]:                       # if exit window from the right : dispawn
            self.auto_destruction()

    def auto_destruction(self):                                                 # Auto-destruct itself
        self.player.rockets.remove(self)
