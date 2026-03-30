from random import choice
from pathlib import Path
from src.vars import *
import pygame.mixer
# import pygame
import os


class SoundManager:
    def __init__(self, amount=0.2):
        pygame.mixer.init()
        self.musics = {                                                         # ogg files
            'bg_music': self.create_list_song("background_music.ogg"),
            'ambiance': self.create_list_song("transfering_data.ogg", "in_a_spaceship.ogg"),
        }
        self.sounds = {                                                         # wav files
            'launch':       self.create_list_song("launch_2.wav", "launch_4.wav"),
            'explosion':    self.create_list_song("explosion1.wav", "explosion2.wav"),
            'shoot':        self.create_list_song("shooting_1.wav", "shooting_2.wav", "shooting_3.wav"),
            'game_over':    self.create_list_song("game_over_mario_version.wav"),
        }
        self.music_volume = 0.1
        self.sound_volume = 0.1
        self.set_volume(amount)

    @staticmethod
    def create_list_song(*args):
        list_songs = []
        for index, name in enumerate(args):
            if not (name.endswith(".mp3") or name.endswith(".ogg") or name.endswith(".wav") or "." in name):
                name += ".ogg"
                # name += ".wav"
            song = Path(filename_sounds) / name
            if os.path.exists(song):
                list_songs.append(song)
        return list_songs

    def play_music(self, name, infinite=False):
        music_name = choice(self.musics[name])
        print(music_name)                                                       # !!!
        pygame.mixer.music.load(music_name)
        self.set_volume(self.music_volume)
        pygame.mixer.music.play(-1 if infinite else 0)

    def play_sound(self, name, infinite=False):
        sound_name = choice(self.sounds[name])
        print(sound_name)                                                       # !!!
        sound = pygame.mixer.Sound(sound_name)
        self.set_volume(self.sound_volume, sound)
        sound.play(-1 if infinite else 0)

    def pause(self, name):
        pygame.mixer.music.pause()
        for sound in self.sounds[name]:
            sound.stop()

    @staticmethod
    def set_volume(amount, sound: pygame.mixer.Sound = None):
        if sound:
            sound.set_volume(amount)
        else:
            pygame.mixer.music.set_volume(amount)
