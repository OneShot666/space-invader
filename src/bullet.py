import pygame


class PlasmaShooter(pygame.sprite.Sprite):
    def __init__(self, player, image=None):
        super().__init__()
        self.damage = 15
        self.speed = 15
        self.cost = 5
        self.player = player
        self.width = self.player.width * 0.2
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.width, (self.width * 1/3) // 1)) if image else None
        # self.mask = pygame.mask.from_surface(self.image)                      # Not optimized -> rect is enough
        self.size = self.image.get_size() if image else (1, 1)
        self.rect = self.image.get_rect() if image else pygame.Rect(0, 0, 1, 1)
        self.rect.x = self.player.rect.x + self.player.width
        self.rect.y = (self.player.rect.y + self.player.height * 0.5) // 1

    def move(self):                                                             # Move rocket + deal dispawn
        self.rect.x += self.speed

        if self.rect.x > self.player.game.screen_size[0]:                       # if exit window from the right : dispawn
            self.auto_destruction()

    def auto_destruction(self):                                                 # Auto-destruct itself
        self.player.Rockets.remove(self)
