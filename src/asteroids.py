# from math import sin
from random import uniform, randint, choice
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
        self.gap =          uniform(0, 0.25) * choice([-1, 1])
        self.xp =           (self.health_max / 10) // 1
        # Image data
        self.width = (self.random * screen_size[0] * 0.05) // 1
        self.height = (self.width * 1) // 1
        self.bar_height = 5
        self.original_image = pygame.transform.scale(image, (self.width, self.height))
        angle = randint(0, 360)
        self.original_image = pygame.transform.rotate(self.original_image, angle)   # Random angle
        self.image = self.original_image
        self.image_size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] + randint(1, 5) * self.image_size[1]
        self.rect.y = randint(0, int(screen_size[1] - self.height))
        self.precise = float(self.rect.y)
        # Damage data
        self.hurt_image = self.image.copy()
        self.hurt_image.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
        self.hit_delay = 100
        self.last_hit_time = 0

    def update_health_bar(self, screen):                                        # Update current life
        pygame.draw.rect(screen, (30, 80, 30), [self.rect.x, self.rect.y - 2 * self.bar_height,
            self.health_max / self.health_max * self.width, self.bar_height])
        pygame.draw.rect(screen, (48, 225, 25), [self.rect.x, self.rect.y - 2 * self.bar_height,
            self.health / self.health_max * self.width, self.bar_height])

    def take_damage(self, amount):                                              # Reduce health
        self.last_hit_time = pygame.time.get_ticks()

        if self.health - amount > amount:
            self.health -= amount
            return False
        else:                                                                   # Give player xp & score when destroyed
            self.health = 0
            self.auto_destruction()
            self.player.gain_experience(self.xp)
            self.player.game.add_score(self.xp)
            return True

    def update_flash(self):
        if pygame.time.get_ticks() - self.last_hit_time <= self.hit_delay:
            self.image = self.hurt_image
        else:
            self.image = self.original_image

    def fall(self):                                                             # Manage collisions + asteroids group + damage
        self.rect.x -= self.speed
        self.precise += self.gap
        self.rect.y = int(self.precise)
        # self.rect.y += math.sin(self.rect.x / 50) * 2                           # Ondulation method

        if self.rect.x + self.image_size[0] < 0:                                # Exit screen from the left
            self.auto_destruction()
            self.player.gain_experience(1)

    def auto_destruction(self):                                                 # Destroy self
        self.player.game.asteroid_belt.Asteroids.remove(self)
