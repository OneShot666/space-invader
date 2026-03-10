import pygame

"""                Variables du jeu                 """
filename_images = 'images'
filename_fonts = 'fonts'
filename_sounds = 'sounds'

game_name = 'Space Invader'
pygame.display.set_caption(game_name, f'{filename_images}/icon.png')
win_width = 1240
win_height = 720

screen = pygame.image.load(f'{filename_images}/background1.png')
screen = pygame.transform.scale(screen, (win_width, win_height))
fond_ecran_taille = screen.get_rect()
taille_fenetre = fond_ecran_taille[2:4]
ecran = pygame.display.set_mode(taille_fenetre)

banniere_side = win_width * 0.2
banniere = pygame.image.load(f'{filename_images}/icon.png')
banniere = pygame.transform.scale(banniere, (banniere_side, banniere_side))
banniere_rect = banniere.get_rect()
banniere_taille = banniere_rect[2:4]

play_button_side = win_width * 0.1
play_button = pygame.image.load(f'{filename_images}/play_button.png')
play_button = pygame.transform.scale(play_button, (play_button_side, play_button_side))
play_button_rect = play_button.get_rect()
bouton_play_taille = play_button_rect[2:4]

level_select_side_x = win_width * 0.4
level_select_side_y = win_width * 0.2
level_select = pygame.image.load(f'{filename_images}/level_select.png')
level_select = pygame.transform.scale(play_button, (level_select_side_x, level_select_side_y))
level_select_rect = play_button.get_rect()
level_select_taille = play_button_rect[2:4]
