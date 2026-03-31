import pygame


class LevelCard:
    def __init__(self, level_id, x, y, width, height, config, font):
        # Level data
        self.level_id = level_id
        self.rect = pygame.Rect(x, y, width, height)
        self.config = config
        # Card data
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)         # Create surface that handle transparency
        bg_color = (30, 30, 50, 150)
        border_color = (100, 100, 250, 200)
        pygame.draw.rect(self.surface, bg_color, (0, 0, width, height), border_radius=15)
        pygame.draw.rect(self.surface, border_color, (0, 0, width, height), width=2, border_radius=15)
        # Text
        title_surf = font.render(f"Level {level_id}", True, (32, 32, 255))
        self.surface.blit(title_surf, (width // 2 - title_surf.get_width() // 2, int(height * 0.1)))
        # Images
        ship_img = pygame.image.load(config["player"]["img"]).convert_alpha()
        ship_img = pygame.transform.scale(ship_img, (100, 80))
        self.surface.blit(ship_img, (width // 2 - 50, int(height * 0.3)))
        bullet_img = pygame.image.load(config["bullet"]["img"]).convert_alpha()
        bullet_img = pygame.transform.scale(bullet_img, (40, 20))
        self.surface.blit(bullet_img, (width // 2 - 20, int(height * 0.55)))
        ast_img = pygame.image.load(config["asteroid"]["img"]).convert_alpha()
        ast_img = pygame.transform.scale(ast_img, (100, 100))
        if config["comet"]:
            self.surface.blit(ast_img, (int(width * 0.3 - 50), int(height * 0.7)))
            cmt_img = pygame.image.load(config["comet"]["img"]).convert_alpha()
            cmt_img = pygame.transform.scale(cmt_img, (100, 100))
            self.surface.blit(cmt_img, (int(width * 0.7 - 50), int(height * 0.7)))
        else:
            self.surface.blit(ast_img, (int(width * 0.5 - 50), int(height * 0.7)))

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
