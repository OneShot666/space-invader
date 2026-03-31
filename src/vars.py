"""                Game variables                 """

# Folders
filename_fonts =  'fonts'
filename_images = 'img'
filename_sounds = 'sounds'

# Sizes
SCREEN_WIDTH = 1240
SCREEN_HEIGHT = 720
banner_size = (SCREEN_WIDTH * 0.2, SCREEN_WIDTH * 0.2)
play_button_size = (SCREEN_WIDTH * 0.1, SCREEN_WIDTH * 0.1)
level_select_size = (SCREEN_WIDTH * 0.2, SCREEN_WIDTH * 0.1)

# Fonts
FONT_NAME = f"{filename_fonts}/CutiveMono-Regular.ttf"

# Images
ICON_NAME =         f'{filename_images}/ui/icon.png'
BG_IMAGE_NAME =     f'{filename_images}/ui/background.png'
BANNER_NAME =       f'{filename_images}/ui/icon.png'
PLAY_BUTTON_NAME =  f'{filename_images}/ui/play_button.png'
LEVEL_SELECT_NAME = f'{filename_images}/ui/level_select.png'
SPACESHIP1_NAME =   f'{filename_images}/spaceships/spaceship1.png'
SPACESHIP2_NAME =   f'{filename_images}/spaceships/spaceship2.png'
SPACESHIP3_NAME =   f'{filename_images}/spaceships/spaceship3.png'
SHIELD_NAME =       f'{filename_images}/shields/beauty shield.png'
BULLET1_NAME =      f"{filename_images}/bullets/rocket1.png"
BULLET2_NAME =      f"{filename_images}/bullets/rocket2.png"
BULLET3_NAME =      f"{filename_images}/bullets/rocket3.png"
ASTEROID1_NAME =    f'{filename_images}/comets/asteroid1.png'
ASTEROID2_NAME =    f'{filename_images}/comets/asteroid2.png'
ASTEROID3_NAME =    f'{filename_images}/comets/asteroid3.png'
COMET1_NAME =       f'{filename_images}/comets/comet1.png'
COMET2_NAME =       f'{filename_images}/comets/comet2.png'

# Levels
LEVELS_DATA = {
    1: {
        "player": {"img": SPACESHIP1_NAME, "speed": 5, "health": 200, "energy": 100, "regen": 0.25, "rate": 0.3},
        "bullet": {"img": BULLET1_NAME, "speed": 15, "damage": 15, "cost": 10},
        "belt": {"density": 30, "max_size": 30, "chaos": 0.25},
        "asteroid": {"img": ASTEROID1_NAME, "speed_range": (1, 5), "hp_mult": (40, 60)},
        "comet": None,
    }, 2: {
        "player": {"img": SPACESHIP2_NAME, "speed": 8, "health": 250, "energy": 150, "regen": 0.5, "rate": 0.2},
        "bullet": {"img": BULLET2_NAME, "speed": 20, "damage": 20, "cost": 15},
        "belt": {"density": 20, "max_size": 40, "chaos": 0.4},
        "asteroid": {"img": ASTEROID2_NAME, "speed_range": (2, 7), "hp_mult": (50, 70)},
        "comet": {"img": COMET1_NAME, "speed_range": (5, 10), "hp_mult": (40, 60)},
    }, 3: {
        "player": {"img": SPACESHIP3_NAME, "speed": 12, "health": 300, "energy": 200, "regen": 1, "rate": 0.1},
        "bullet": {"img": BULLET3_NAME, "speed": 5, "damage": 25, "cost": 20},
        "belt": {"density": 15, "max_size": 50, "chaos": 0.55},
        "asteroid": {"img": ASTEROID3_NAME, "speed_range": (3, 9), "hp_mult": (75, 100)},
        "comet": {"img": COMET2_NAME, "speed_range": (7, 12), "hp_mult": (30, 50)},
    },
}
