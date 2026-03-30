from src.vars import SPACESHIP1_NAME, BULLET_NAME
from src.bullet import PlasmaShooter
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        # Stats data
        self.health =       200
        self.health_max =   200
        self.energy =       0
        self.energy_max =   100
        self.xp =           0
        self.xp_max =       100
        self.speed =        10
        self.regen_amount = 0.2
        # Image data
        self.width = (game.screen_size[0] * 0.1) // 1
        self.height = (self.width * 0.5) // 1
        self.bar_height = (self.height * 0.1) // 1
        self.image =    pygame.image.load(SPACESHIP1_NAME).convert_alpha()
        self.image =    pygame.transform.scale(self.image, (self.width, self.height))
        self.mask =     pygame.mask.from_surface(self.image)
        self.rect =     self.image.get_rect()
        self.rect.x =   self.width
        self.rect.y =   (game.screen_size[1] * 0.5 - self.height * 0.5) // 1
        # Bullet data
        self.bullet_image = pygame.image.load(BULLET_NAME).convert_alpha()
        self.Rockets = pygame.sprite.Group()

    def update_bar(self, surface, current, maximum, color, max_color, coeff=1): # Any bar
        pygame.draw.rect(surface, max_color, [self.rect.x, self.rect.y - coeff * self.bar_height,
            self.width, self.bar_height])
        pygame.draw.rect(surface, color, [self.rect.x, self.rect.y - coeff * self.bar_height,
            current / maximum * self.width, self.bar_height])

    def update_health_bar(self, surface):                                       # Barre de vie
        self.update_bar(surface, self.health, self.health_max, (48, 225, 25), (30, 80, 30), 4)

        if self.health < self.health_max * 0.1:
            print("Attention Commandant, la coque est gravement touchée !")

    def update_energy_bar(self, surface):                                       # Barre d'énergie
        self.update_bar(surface, self.energy, self.energy_max, (0, 205, 255), (0, 95, 245), 3)

    def update_xp_bar(self, surface):                                           # Barre d'xp
        self.update_bar(surface, self.xp, self.xp_max, (255, 215, 0), (120, 90, 0), 2)

    def hurt(self, amount):                                                     # Take damages
        if self.health - amount > amount:
            self.health -= amount
            print(f"Damage taken ! ({amount})")
        else:
            self.game.game_over()

    def regen_energy(self, coeff=1):
        if self.energy + self.regen_amount <= self.energy_max:
            self.energy += self.regen_amount
        else:
            self.energy = self.energy_max

    def gain_experience(self, amount):
        self.xp += amount

        while self.xp > self.xp_max:
            self.level_up()

    def level_up(self):
        self.xp -= self.xp_max
        self.xp_max += 50
        self.health = self.health_max
        self.energy = self.energy_max
        self.game.rocket.damage += 5
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
        self.game.sound_manager.play_sound("shoot")
        self.Rockets.add(PlasmaShooter(self, self.bullet_image))
