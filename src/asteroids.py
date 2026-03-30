from random import uniform, randint
from src.player import Player
import pygame


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen_size, player: Player, image):
        super().__init__()
        self.player = player
        # Attributes
        self.random =       uniform(0.5, 2.5)                                   # Random profile
        self.health =       (self.random * 50) // 1
        self.health_max =   (self.random * 50) // 1
        self.damage =       self.random * 20 // 1
        self.speed =        uniform(1, 5)
        self.xp =           (self.health_max / 10) // 1
        # Image data
        self.width = (self.random * screen_size[0] * 0.05) // 1
        self.height = (self.width * 1) // 1
        self.bar_height = 5
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.image_size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] + randint(1, 5) * self.image_size[1]
        self.rect.y = screen_size[1] / 100 * randint(0, 100)

    def update_health_bar(self, screen):                                        # Update current life
        pygame.draw.rect(screen, (30, 80, 30), [self.rect.x, self.rect.y - 2 * self.bar_height,
            self.health_max / self.health_max * self.width, self.bar_height])
        pygame.draw.rect(screen, (48, 225, 25), [self.rect.x, self.rect.y - 2 * self.bar_height,
            self.health / self.health_max * self.width, self.bar_height])

    def take_damage(self, amount):                                              # Reduce health
        if self.health - amount > amount:
            self.health -= amount
        else:                                                                   # Give player xp & score when destroyed
            self.health = 0
            self.auto_destruction()
            self.player.gain_experience(self.xp)
            self.player.game.add_score(self.xp)
            print(f"Astéroide détruit ! (+{self.xp}xp)")
            print(f"Score : {self.player.game.score} pts")

    def fall(self):                                                             # Manage collisions + asteroids group + damage
        self.rect.x -= self.speed

        if self.rect.x + self.image_size[0] < 0:                                # Exit screen from the left
            self.auto_destruction()
            self.player.gain_experience(1)
            print("Ouf, on a évité un astéroide !")

    def auto_destruction(self):                                                 # Destroy self
        self.player.game.asteroid_belt.Asteroids.remove(self)
