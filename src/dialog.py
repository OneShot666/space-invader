# import pygame.sprite
from vars import *


# ! Add list in game to deal with notification (max : 3, stay on screen for 5 sec, fade away : set_alpha)
class DialogBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = None
        self.position = None
        self.message = None

    def new_message(self, message, position=None, size=20):
        if position is None:
            position = [win_width * 0.5, win_height * 0.1]
        self.message = message
        self.position = position
        self.font = pygame.font.Font(f"{filename_fonts}/CutiveMono-Regular.ttf", size)
        self.display()

    def display(self, color=(255, 255, 255)):
        text = self.font.render(self.message, True, color)
        ecran.blit(text, self.position)
