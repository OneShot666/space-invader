from src.vars import SHIELD_NAME, FONT_NAME
from src.bullet import PlasmaShooter
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game, config, bullet_config):
        super().__init__()
        self.game = game
        self.config = config
        self.bullet_config = bullet_config
        self.is_following = True
        self.is_shielding = False
        # Stats data
        self.health =       config["health"]
        self.health_max =   config["health"]
        self.energy =       config["energy"]
        self.energy_max =   config["energy"]
        self.regen_amount = config["regen"]
        self.speed =        config["speed"]
        self.xp =           0
        self.xp_max =       100
        self.shoot_delay =  config["rate"] * 1000                               # Ms between shoots
        # Image data
        self.width =  (game.screen_size[0] * 0.1) // 1
        self.height = (self.width * 0.5) // 1
        self.bar_height = (self.height * 0.1) // 1
        self.original_image = pygame.image.load(config["img"]).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.image =    self.original_image
        self.mask =     pygame.mask.from_surface(self.image)
        self.rect =     self.image.get_rect()
        self.rect.x =   self.width
        self.rect.y =   (game.screen_size[1] * 0.5 - self.height * 0.5) // 1
        # Damage data
        self.hurt_image = self.image.copy()
        self.hurt_image.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
        self.base_delay = 20
        self.hit_delay = 0
        self.last_hit_time = 0
        # Shield data
        self.shield_cost = 2
        self.shield_image = pygame.image.load(SHIELD_NAME).convert_alpha()
        self.shield_image = pygame.transform.scale(self.shield_image, (self.width * 2, self.height * 2))
        self.shield_image.fill((255, 255, 255, 96), special_flags=pygame.BLEND_RGBA_MULT)
        # Bullet data
        self.last_shot = 0
        self.bullet_image = pygame.image.load(bullet_config["img"]).convert_alpha()
        self.rocket = PlasmaShooter(self, self.bullet_image, bullet_config)     # Example of bullet
        self.Bullets = pygame.sprite.Group()
        # Warning data
        self.warning_font = pygame.font.Font(FONT_NAME, 30)
        self.warning_symbol = '!'
        self.set_center()

    def set_center(self):
        raw_x, raw_y = pygame.mouse.get_pos()

        try:
            logic_x, logic_y = self.game.screen.get_rect().topleft
            target_x = max(0, min(raw_x, self.game.screen_size[0]))
            target_y = max(0, min(raw_y, self.game.screen_size[1]))
            self.rect.center = (target_x, target_y)
        except:
            self.rect.center = (raw_x, raw_y)

    def update_bar(self, surface, current, maximum, color, max_color, coeff=1, warning=False):  # Any bar
        y = self.rect.y - coeff * self.bar_height
        pygame.draw.rect(surface, max_color, [self.rect.x, y, self.width, self.bar_height])
        pygame.draw.rect(surface, color, [self.rect.x, y, current / maximum * self.width, self.bar_height])

        if warning and current < maximum * 0.2:
            if (pygame.time.get_ticks() // 250) % 2:                            # Make text blink based on time
                warning_text = self.warning_font.render(self.warning_symbol, True, color)
                surface.blit(warning_text, (self.rect.x - 20, y - 12))

    def update_health_bar(self, surface):                                       # Barre de vie
        self.update_bar(surface, self.health, self.health_max, (48, 225, 25), (30, 80, 30), 4, True)

    def update_energy_bar(self, surface):                                       # Barre d'énergie
        self.update_bar(surface, self.energy, self.energy_max, (0, 205, 255), (0, 95, 245), 3, True)

    def update_xp_bar(self, surface):                                           # Barre d'xp
        self.update_bar(surface, self.xp, self.xp_max, (255, 215, 0), (120, 90, 0), 2)

    def update_flash(self):
        if pygame.time.get_ticks() - self.last_hit_time <= self.hit_delay:
            self.image = self.hurt_image
        else:
            self.image = self.original_image

    def draw(self, screen, offset=(0, 0)):
        self.update_flash()

        for bullet in self.Bullets:
            screen.blit(bullet.image, (bullet.rect.x + offset[0], bullet.rect.y + offset[1]))

        self.update_health_bar(screen)
        self.update_energy_bar(screen)
        self.update_xp_bar(screen)

        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

        if self.is_shielding:
            self.energy -= self.shield_cost
            screen.blit(self.shield_image, (int(self.rect.x - self.width * 0.5 + offset[0]),
                int(self.rect.y - self.height * 0.5 + offset[1])))

        if self.energy < self.shield_cost:
            self.is_shielding = False

    def hurt(self, amount):                                                     # Take damages
        now = pygame.time.get_ticks()
        if now - self.last_hit_time > self.hit_delay:
            self.last_hit_time = now
            self.hit_delay = amount * self.base_delay
            if self.health - amount > amount:
                self.health -= amount
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
        self.xp_max += 10
        self.health = self.health_max
        self.energy = self.energy_max
        self.rocket.damage += 5
        print("Level Up !")                                                     # ! Play sound

    def follow_mouse(self):
        mouse_x, mouse_y = self.game.get_web_mouse_pos()
        center_y = self.rect.centery                                            # Get player center
        center_x = self.rect.centerx

        if abs(center_y - mouse_y) > self.speed:                                # Fluid movement
            if center_y < mouse_y: self.move_down()
            else: self.move_up()
        if abs(center_x - mouse_x) > self.speed:
            if center_x < mouse_x: self.move_right()
            else: self.move_left()

    def move_up(self):                                                         # Déplacements
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):                                                           # Attaque
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and self.energy >= self.rocket.cost and not self.is_shielding:   # If can shoot
            self.game.sound_manager.play_sound("shoot")
            self.Bullets.add(PlasmaShooter(self, self.bullet_image, self.bullet_config))
            self.energy -= self.rocket.cost
            self.last_shot = now

    def toggle_shield(self):
        self.is_shielding = not self.is_shielding
        if self.energy < self.shield_cost:
            self.is_shielding = False
