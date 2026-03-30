import pygame

"""                Variables du jeu                 """
filename_fonts = 'fonts'
filename_images = 'img'
filename_sounds = 'sounds'

game_name = 'Space Invader'
pygame.display.set_caption(game_name, f'{filename_images}/ui/icon.png')
win_width = 1240
win_height = 720

bg_image = pygame.image.load(f'{filename_images}/ui/background1.png')
bg_image = pygame.transform.scale(bg_image, (win_width, win_height))
bg_image_size = bg_image.get_rect()
screen_size = bg_image_size[2:4]
screen = pygame.display.set_mode(screen_size)

banner_side = win_width * 0.2
banner = pygame.image.load(f'{filename_images}/ui/icon.png')
banner = pygame.transform.scale(banner, (banner_side, banner_side))
banner_rect = banner.get_rect()
banner_size = banner_rect[2:4]

play_button_side = win_width * 0.1
play_button = pygame.image.load(f'{filename_images}/ui/play_button.png')
play_button = pygame.transform.scale(play_button, (play_button_side, play_button_side))
play_button_rect = play_button.get_rect()
bouton_play_size = play_button_rect[2:4]

level_select_side_x = win_width * 0.4
level_select_side_y = win_width * 0.2
level_select = pygame.image.load(f'{filename_images}/ui/level_select.png')
level_select = pygame.transform.scale(level_select, (level_select_side_x, level_select_side_y))
level_select_rect = level_select.get_rect()
level_select_size = level_select_rect[2:4]
