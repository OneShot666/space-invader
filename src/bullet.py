import pygame


class PlasmaShooter(pygame.sprite.Sprite):
    def __init__(self, player, image, config):
        super().__init__()
        self.level = 1
        self.damage =   config["damage"]
        self.speed =    config["speed"]
        self.cost =     config["cost"]
        self.player =   player
        self.width =    self.player.width * 0.2
        self.image =    image
        self.image = pygame.transform.scale(self.image, (self.width, (self.width * 1/3) // 1))
        # self.mask = pygame.mask.from_surface(self.image)                      # Not optimized -> rect is enough
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x + self.player.width
        self.rect.y = (self.player.rect.y + self.player.height * 0.5) // 1

    def move(self):                                                             # Move rocket + deal dispawn
        self.rect.x += self.speed

        if self.rect.x > self.player.game.screen_size[0]:                       # if exit window from the right : dispawn
            self.auto_destruction()

    def auto_destruction(self):                                                 # Auto-destruct itself
        self.player.Bullets.remove(self)
