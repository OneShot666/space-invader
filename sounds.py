import pygame


class SoundManager:
    def __init__(self, amount=0.5):
        pygame.mixer.init()
        self.sounds = {
            'background_music': pygame.mixer.Sound("Sons/music_fond.ogg"),
            'launch': pygame.mixer.Sound("Sons/decollage_spaceship1.mp3"),
            'explosion': pygame.mixer.Sound("Sons/explosion1.mp3"),
            'shoot': pygame.mixer.Sound("Sons/tir_laser1.mp3"),
            'game_over': pygame.mixer.Sound("Sons/game_over_mario_version.wav")
        }
        self.set_all_volume(amount)

    def play(self, name):
        self.sounds[name].play()

    def pause(self, name):
        self.sounds[name].stop()

    def set_volume(self, name, amount):
        self.sounds[name].set_volume(amount)

    def set_all_volume(self, amount):
        for sound, name in self.sounds.items():
            self.set_volume(name, amount)
