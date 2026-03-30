from pathlib import Path
from random import choice
from src.vars import filename_sounds
import pygame
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
            'shoot':        self.create_list_song("shooting_1.wav", "shooting_2.wav", "shooting_3.wav"),
            'explosion':    self.create_list_song("explosion1.wav", "explosion2.wav"),
            'game_over':    self.create_list_song("game_over_mario_version.wav"),
        }
        self.music_volume = 0.1
        self.sound_volume = 0.1
        self.set_volume(amount)

    @staticmethod
    def create_list_song(*args):
        list_songs = []
        for index, name in enumerate(args):
            song_name = Path(filename_sounds) / name
            if os.path.exists(song_name):
                if name.endswith(".ogg"):
                    list_songs.append(song_name)
                elif name.endswith(".wav"):
                    song = pygame.mixer.Sound(song_name)
                    list_songs.append(song)
        return list_songs

    def play_music(self, name, infinite=False):
        music_name = choice(self.musics[name])
        pygame.mixer.music.load(music_name)
        self.set_volume(self.music_volume)
        pygame.mixer.music.play(-1 if infinite else 0)

    def play_sound(self, name, infinite=False):
        sound = choice(self.sounds[name])
        self.set_volume(self.sound_volume, sound)
        sound.play(-1 if infinite else 0)

    def pause(self, name=None):
        pygame.mixer.music.pause()
        if name:
            for sound in self.sounds[name]:
                sound.stop()

    @staticmethod
    def set_volume(amount, sound: pygame.mixer.Sound = None):
        if sound:
            sound.set_volume(amount)
        else:
            pygame.mixer.music.set_volume(amount)
