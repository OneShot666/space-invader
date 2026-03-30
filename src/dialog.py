from src.vars import *
import pygame.sprite


# ! Add list in game to deal with notification (max : 3, stay on screen for 5 sec, fade away : set_alpha)
class DialogBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = None
        self.position = None
        self.message = None

    def new_message(self, screen, message, position=None, size=20):
        if position is None:
            position = [SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.1]
        self.message = message
        self.position = position
        self.font = pygame.font.Font(FONT_NAME, size)
        self.display(screen)

    def display(self, screen, color=(255, 255, 255)):
        text = self.font.render(self.message, True, color)
        screen.blit(text, self.position)
