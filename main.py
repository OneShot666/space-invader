from src.asteroid_belt import AsteroidBelt
from src.bullet import PlasmaShooter
from src.sounds import SoundManager
from src.dialog import DialogBox
from src.player import Player
from src.vars import *
import asyncio
import pygame


# [v0.0.6] . Add message box in game (all print content) + put score behind player & belt
# [v0.0.7] ! Allow to hold SPACE pressed to shoot + mouse moving option + nb max of asteroids
# [v0.0.8] ! Add levels + level manager + shield (right click -> cost energy)
# [v0.0.9] L Add death screen + go back to main menu
# [v0.1.0] L Add upgrades for spaceship & asteroids
# [v0.1.1] L Add balancing (speed, size, HP, etc)
class Game:
    def __init__(self):
        pygame.init()
        # Game data
        self.name = "Space Invader"
        self.creator = "One Shot"
        self.version = "v0.0.5"
        self.birthday = "19/11/2022"
        # Bool data
        self.game_in_progress = True
        self.menu_in_progress = True
        self.lvl1_in_progress = False                                           # L Replace by current_level
        self.lvl2_in_progress = False
        self.lvl3_in_progress = False
        self.music_on =         True
        # Screen data
        self.bg_image =     None
        self.screen =       None
        self.screen_size =  None
        self.banner =       None
        self.banner_size =  None
        # Buttons data
        self.play_button =          None
        self.play_button_size =     None
        self.select_button =        None
        self.select_button_size =   None
        # Gameplay data
        self.pressed = {}
        self.Players = pygame.sprite.Group()
        self.player = None
        self.rocket = None
        # self.asteroids = pygame.sprite.Group()
        self.asteroid_group = None
        self.score = 0
        # Font & Music data
        self.font = None
        self.sound_manager = None
        self.song_name = "bg_music"                                             # Sound category
        self.dialogs_wait_list = []
        self.dialog = None
        # Function
        # self.Run()

    def load_ressources(self):
        self.create_screen()
        self.create_banner()
        self.create_buttons()
        pygame.display.set_caption(game_name, ICON_NAME)                        # Set icon
        self.player = Player(self)
        self.Players.add(self.player)
        self.rocket = PlasmaShooter(self.player)
        self.asteroid_group = AsteroidBelt(self.screen_size, self.player)
        self.font = pygame.font.Font(FONT_NAME, 50)
        self.sound_manager = SoundManager()
        self.dialog = DialogBox()

    def create_screen(self):
        bg_image = pygame.image.load(BG_IMAGE_NAME)
        self.bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image_size = self.bg_image.get_rect()
        self.screen_size = bg_image_size[2:4]
        self.screen = pygame.display.set_mode(self.screen_size, pygame.SCALED)

    def create_banner(self):
        banner = pygame.image.load(BANNER_NAME)
        self.banner = pygame.transform.scale(banner, banner_size)
        banner_rect = self.banner.get_rect()
        self.banner_size = banner_rect[2:4]

    def create_buttons(self):
        play_button = pygame.image.load(PLAY_BUTTON_NAME)
        self.play_button = pygame.transform.scale(play_button, play_button_size)
        play_button_rect = self.play_button.get_rect()
        self.play_button_size = play_button_rect[2:4]

        # Level selector data
        # level_select = pygame.image.load(LEVEL_SELECT_NAME)                   # L Not yet
        # self.select_button = pygame.transform.scale(level_select, level_select_size)
        # level_select_rect = self.select_button.get_rect()
        # self.select_button_size = level_select_rect[2:4]

    async def Run(self):
        await asyncio.sleep(1)

        self.load_ressources()
        await asyncio.sleep(0)

        print(f"Lancement du jeu {game_name} !")
        if self.music_on:
            self.sound_manager.play_music(self.song_name, True)

        while self.game_in_progress:
            self.screen.blit(self.bg_image, (0, 0))
            await self.inputs()

            if self.lvl1_in_progress:  # Niveau 1 en cours...
                # print("Entrer dans la boucle")
                self.update_game()
            elif self.lvl2_in_progress:  # Niveau 2 en cours...
                self.update_game()
            elif self.lvl3_in_progress:  # Niveau 3 en cours...
                self.update_game()
            else:  # Menu principal
                banner_rect = self.banner.get_rect()
                banner_rect.x = (self.screen_size[0] * 0.5 - self.banner_size[0] * 0.5) // 1
                banner_rect.y = (self.screen_size[1] * 0.35 - self.banner_size[1] * 0.5) // 1
                self.screen.blit(self.banner, banner_rect)
                play_button_rect = self.play_button.get_rect()
                play_button_rect.x = (self.screen_size[0] * 0.5 - self.play_button_size[0] * 0.5) // 1
                play_button_rect.y = (self.screen_size[1] * 0.45 + self.banner_size[1] * 0.5) // 1
                self.screen.blit(self.play_button, play_button_rect)
            """ elif jeu.menu_in_progress:                                          # Sélection des niveaux
                for i in range(3):
                    level_select_rect.x = (taille_fenetre[0] * 0.5 - level_select_taille[0] * 0.5) // 1
                    level_select_rect.y = i * (taille_fenetre[1] * 0.1 + level_select_taille[1]) // 1
                    ecran.blit(level_select, level_select_rect)
                    lvl_text = jeu.font.render(f"Niveau {i + 1}", True, (0, 0, 0))  # Affiche les niveaux
                    ecran.blit(lvl_text, (level_select_rect.x * 0.5, level_select_rect.y * 0.5))  # Position du texte
            """

            pygame.display.flip()

            await asyncio.sleep(0)

    async def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.pressed[event.key] = True  # Active les touches pressées

                if event.key == pygame.K_RETURN:  # Ouvre le menu (touche)
                    await self.menu()

                if event.key == pygame.K_ESCAPE:                                # ! Comment before pushing
                    self.close_game()

                if event.key == pygame.K_m:  # On/Off la musique du jeu
                    self.mute_musics()

            if event.type == pygame.KEYUP:  # Désactive les touches relachées
                self.pressed[event.key] = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # Ouvre le menu (bouton)
                play_button_rect = self.play_button.get_rect()
                if play_button_rect.collidepoint(event.pos):
                    await self.menu()
                    # game.sound_manager.play("background_music")

            if event.type == pygame.QUIT:
                self.close_game()

    async def menu(self, level=1):                                              # Manage main menu
        self.game_in_progress = True
        self.sound_manager.play_sound("launch")
        print(f"Décollage ! (level {level})")
        await asyncio.sleep(2)

        if self.menu_in_progress:
            if level == 1:
                print("Chargement du level 1 : ")
                self.lvl1_in_progress = True
            elif level == 2:
                self.lvl2_in_progress = True
            elif level == 3:
                self.lvl3_in_progress = True
            else:
                print(f"AI : <error! level {level} doesn't exist>")
                print("Bon bah, atterissage alors..")
                self.menu_in_progress = False

    def update_game(self):  # Met le jeu à jour
        self.screen.blit(self.player.image, self.player.rect)

        self.player.update_health_bar(self.screen)
        self.player.update_energy_bar(self.screen)
        self.player.update_xp_bar(self.screen)

        self.player.take_energy(self.player.regen_energy)

        for rocket in self.player.rockets:  # Gère mouvements tirs laser
            rocket.move()

        for asteroid in self.asteroid_group.asteroids:  # Gère vie et mouvement des astéroides
            asteroid.update_health_bar(self.screen)
            asteroid.fall()

        self.player.rockets.draw(self.screen)  # Dessine les tirs du joueur
        self.asteroid_group.asteroids.draw(self.screen)  # Dessine les astéroïdes
        self.asteroid_group.start_event()  # Créer un astéroïde toutes les 0.15 sec ?

        #        font = pygame.font.SysFont("monospace", 16)                            # Créer la police(nom, taille)
        score_text = self.font.render(f"Score : {int(self.score)}", True, (255, 255, 255))  # Affiche le score
        self.screen.blit(score_text, (self.screen_size[0] * 0.5, self.screen_size[1] * 0.1))  # Position du score

        if self.pressed.get(pygame.K_UP) and self.player.rect.y > 0:  # Déplacement du joueur
            self.player.move_up()
            print("Montez !")
        elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y + self.player.rect.height < self.screen_size[1]:
            self.player.move_down()
            print("Descendez !")

        if self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
            print("Reculez !")
        elif self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < self.screen_size[0]:
            self.player.move_right()
            print("Avancez !")

        if self.pressed.get(pygame.K_SPACE):
            if self.rocket.cost <= self.player.energy:                          # Attaque si a l'énergie
                self.player.energy -= self.rocket.cost
                self.player.shoot()
                self.pressed[pygame.K_SPACE] = False
                print("Piou piou !")
            else:
                self.pressed[pygame.K_SPACE] = False
                print("Pas assez d'énergie !")

    def add_score(self, value=100):
        self.score += value

        if self.score < 0:
            self.score = 0

    @staticmethod
    def check_collision(sprite, group):  # Vérifie si un astéroide touche le joueur
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def mute_musics(self):
        self.music_on = not self.music_on
        infinite = True if self.song_name == "bg_music" else False

        if self.music_on:
            print(f"Musique activée : '{self.song_name}'")
            self.sound_manager.play_music(self.song_name, infinite)
        else:
            print(f"Musique désactivée : '{self.song_name}'")
            self.sound_manager.pause(self.song_name)

    def go_to_menu(self):
        self.game_in_progress = False
        self.menu_in_progress = True
        self.check_booleen()

    def check_booleen(self):
        print("Vérification des booléens...")
        if self.game_in_progress:
            self.menu_in_progress = False
            self.lvl1_in_progress = False
            self.lvl2_in_progress = False
            self.lvl3_in_progress = False
        elif self.menu_in_progress:
            self.game_in_progress = False
        elif self.lvl1_in_progress:
            self.game_in_progress = False
            self.menu_in_progress = False
            self.lvl2_in_progress = False
            self.lvl3_in_progress = False
        elif self.lvl2_in_progress:
            self.game_in_progress = False
            self.menu_in_progress = False
            self.lvl1_in_progress = False
            self.lvl3_in_progress = False
        elif self.lvl3_in_progress:
            self.game_in_progress = False
            self.menu_in_progress = False
            self.lvl1_in_progress = False
            self.lvl2_in_progress = False

    async def game_over(self):                                                  # Reset game
        self.sound_manager.play_sound("game_over")
        self.player.health = self.player.health_max
        self.player.energy = self.player.energy_max
        self.player.xp = 0
        self.player.xp_max = 100
        self.asteroid_group.asteroids = pygame.sprite.Group()
        self.score = 0
        print("Votre vaisseau a été détruit !")
        await asyncio.sleep(1)

        self.go_to_menu()

    def close_game(self):
        self.game_in_progress = False                                           # L Replace with death screen


async def start_game():
    game = Game()
    await game.Run()

if __name__ == "__main__":
    asyncio.run(start_game())
