from src.vars import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_NAME
import pygame.sprite


# ! Add list in game to deal with notification (max : 3, stay on screen for 5 sec, fade away : set_alpha)
class DialogBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font_size = 0
        self.font = pygame.font.Font(FONT_NAME, 0)
        self.position = None
        self.message =  None

    def new_message(self, screen, message, position=None, size=20, color=(255, 255, 255)):
        if position is None:
            position = [SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.1]
        self.message = message
        self.position = position
        if size != self.font_size:
            self.font = pygame.font.Font(FONT_NAME, size)
            self.font_size = size
        self.display(screen, color)

    def display(self, screen, color=(255, 255, 255)):
        text = self.font.render(self.message, True, color)
        screen.blit(text, self.position)
