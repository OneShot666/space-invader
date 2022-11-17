# import pygame
from random import choice
from vars import *


class SoundManager:
    def __init__(self, amount=0.2):
        pygame.mixer.init()
        self.sounds = {
            'background_music': self.create_list_song("music_fond.ogg", "Cognitive Bias - This Other Space"),
            'launch': self.create_list_song("decollage_spaceship1", "decollage_spaceship2", "decollage_spaceship3",
                                            "decollage_spaceship4"),
            'explosion': self.create_list_song("explosion1", "explosion2"),
            'shoot': self.create_list_song("tir_laser1", "tir_laser2", "tir_laser3"),
            'game_over': self.create_list_song("game_over_mario_version.wav")
        }
        self.set_all_volume(amount)

    @staticmethod
    def create_list_song(*args):
        list_songs = []
        for index, name in enumerate(args):
            if not (name.endswith(".mp3") or name.endswith(".ogg") or name.endswith(".wav") or "." in name):
                name += ".mp3"
            song = pygame.mixer.Sound(f"{filename_sounds}/{name}")
            list_songs.append(song)
        return list_songs

    def play(self, name, infinite=False):
        if infinite:
            choice(self.sounds[name]).play(-1)
        else:
            choice(self.sounds[name]).play()

    def pause(self, name):
        for sound in self.sounds[name]:
            sound.stop()

    def set_volume(self, name, amount):
        for sound in self.sounds[name]:
            sound.set_volume(amount)

    def set_all_volume(self, amount):
        for name, sound in self.sounds.items():
            self.set_volume(name, amount)
