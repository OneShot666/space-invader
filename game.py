from time import *
from event_asteroids1 import *
from player1 import *
from rocket1 import *
from sounds import *


# ! Faire fonction message
# ! Améliorer structure code + class asteroids & events
# ! Finir upgrade spaceships + asteroids
# ! Ajouter musics (dossier d'Algieba)
class Game:
    def __init__(self):
        pygame.init()
        self.game_in_progress = True
        self.menu_in_progress = True
        self.lvl1_in_progress = False
        self.lvl2_in_progress = False
        self.lvl3_in_progress = False
        self.music_on_off = True
        self.pressed = {}
        self.players = pygame.sprite.Group()
        self.joueur = Player1(self)
        self.players.add(self.joueur)
        self.rocket = PlasmaShooter1(self.joueur)
#        self.asteroids = pygame.sprite.Group()
        self.asteroid_group = AsteroidGroup1(self)
        self.font = pygame.font.Font(f"{filename_fonts}/CutiveMono-Regular.ttf", 50)
        self.score = 0
        self.sound_manager = SoundManager()
        self.start()

    def start(self):
        print(f"Lancement du jeu {game_name} !")
        while self.game_in_progress:
            ecran.blit(fond_ecran, (0, 0))

            if self.music_on_off:
                self.sound_manager.play("background_music")

            if self.lvl1_in_progress:                                           # Niveau 1 en cours...
                # print("Entrer dans la boucle")
                self.update_game()
            elif self.lvl2_in_progress:                                         # Niveau 2 en cours...
                self.update_game()
            elif self.lvl3_in_progress:                                         # Niveau 3 en cours...
                self.update_game()
            else:                                                               # Menu principal
                banniere_rect.x = (taille_fenetre[0] * 0.5 - banniere_taille[0] * 0.5) // 1
                banniere_rect.y = (taille_fenetre[1] * 0.35 - banniere_taille[1] * 0.5) // 1
                ecran.blit(banniere, banniere_rect)
                play_button_rect.x = (taille_fenetre[0] * 0.5 - bouton_play_taille[0] * 0.5) // 1
                play_button_rect.y = (taille_fenetre[1] * 0.45 + banniere_taille[1] * 0.5) // 1
                ecran.blit(play_button, play_button_rect)
            """ elif jeu.menu_in_progress:                                                 # Sélection des niveaux
                for i in range(3):
                    level_select_rect.x = (taille_fenetre[0] * 0.5 - level_select_taille[0] * 0.5) // 1
                    level_select_rect.y = i * (taille_fenetre[1] * 0.1 + level_select_taille[1]) // 1
                    ecran.blit(level_select, level_select_rect)
                    lvl_text = jeu.font.render(f"Niveau {i + 1}", True, (0, 0, 0))     # Affiche les niveaux
                    ecran.blit(lvl_text, (level_select_rect.x * 0.5, level_select_rect.y * 0.5))  # Position du texte
            """

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True                              # Active les touches pressées

                    if event.key == pygame.K_RETURN:                            # Ouvre le menu (touche)
                        self.menu()

                    if event.key == pygame.K_m:                                 # On/Off la musique du jeu
                        self.music_on_off = not self.music_on_off

                        if self.music_on_off:
                            print("Musique du jeu activée !")
                        else:
                            print("Musique du jeu désactivée !")

                    if event.key == pygame.K_q:  # Quitte le jeu
                        print("Vous avez quitté le jeu.")
                        self.close_game()

                if event.type == pygame.KEYUP:  # Désactive les touches relachées
                    self.pressed[event.key] = False

                if event.type == pygame.MOUSEBUTTONDOWN:  # Ouvre le menu (bouton)
                    if play_button_rect.collidepoint(event.pos):
                        # jeu.commande()
                        self.menu()
                        self.sound_manager.play("launch")
                        # jeu.sound_manager.play("background_music")

                if event.type == pygame.QUIT:
                    self.close_game()

    @staticmethod
    def commande():
        print("Commandes :")
        sleep(1)
        print("Lancer le jeu : Entrée")
        sleep(1)
        print("Déplacement du vaisseau : Flèches directionnelles")
        sleep(1)
        print("Tirer : Barre espace")
        sleep(1)
        print("Quitter le jeu : touche Q\n")
        sleep(3)

    def menu(self, level=1):                                                  # Gère le menu principal
        self.game_in_progress = True
        print(f"Décollage ! (level {level})")
        sleep(2)
        if self.menu_in_progress:
            if level == 1:
                print("Chargement du level 1 : ")
                self.lvl1_in_progress = True
            elif level == 2:
                self.lvl2_in_progress = True
            elif level == 3:
                self.lvl3_in_progress = True
            else:
                print(f"<error! level {level} doesn't exist>")
                print("Bon bah, atterissage alors..")
                self.menu_in_progress = False

    def game_over(self):                                                       # Réinitialise le jeu
        self.sound_manager.play("game_over")
        self.joueur.health = self.joueur.health_max
        self.joueur.energy = self.joueur.energy_max
        self.joueur.xp = 0
        self.joueur.xp_max = 100
        self.asteroid_group.asteroids = pygame.sprite.Group()
        self.score = 0
        self.game_in_progress = False
        self.check_booleen()
        print("Votre vaisseau a été détruit !")
        sleep(1)

    def update_game(self):                                                     # Met le jeu à jour
        ecran.blit(self.joueur.image, self.joueur.rect)

        self.joueur.update_health_bar(ecran)
        self.joueur.update_energy_bar(ecran)
        self.joueur.update_xp_bar(ecran)

        self.joueur.take_energy(self.joueur.regen_energy)

        for rocket in self.joueur.rockets:                                     # Gère mouvements tirs laser
            rocket.move()

        for asteroid in self.asteroid_group.asteroids:                         # Gère vie et mouvement des astéroides
            asteroid.update_health_bar(ecran)
            asteroid.chute()

        self.joueur.rockets.draw(ecran)                                        # Dessine les tirs du joueur
        self.asteroid_group.asteroids.draw(ecran)                              # Dessine les astéroïdes
        self.asteroid_group.start_event()                                      # Créer un astéroïde toutes les 0.15 sec ?

#        font = pygame.font.SysFont("monospace", 16)                            # Créer la police(nom, taille)
        score_text = self.font.render(f"Score : {int(self.score)}", True, (255, 255, 255))  # Affiche le score
        ecran.blit(score_text, (taille_fenetre[0] * 0.5, taille_fenetre[1] * 0.1))  # Position du score

        if self.pressed.get(pygame.K_UP) and self.joueur.rect.y > 0:           # Déplacement du joueur
            self.joueur.move_up()
            print("Montez !")
        elif self.pressed.get(pygame.K_DOWN) and self.joueur.rect.y + self.joueur.rect.height < taille_fenetre[1]:
            self.joueur.move_down()
            print("Descendez !")

        if self.pressed.get(pygame.K_LEFT) and self.joueur.rect.x > 0:
            self.joueur.move_left()
            print("Reculez !")
        elif self.pressed.get(pygame.K_RIGHT) and self.joueur.rect.x + self.joueur.rect.width < taille_fenetre[0]:
            self.joueur.move_right()
            print("Avancez !")

        if self.pressed.get(pygame.K_SPACE):                                   # Attaque si a l'énergie
            if self.rocket.cost <= self.joueur.energy:
                self.joueur.energy -= self.rocket.cost
                self.joueur.shoot()
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
    def check_collision(sprite, group):                                  # Vérifie si un astéroide touche le joueur
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def check_booleen(self):
        print("Vérifie booléens")
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
        else:
            print("<error! booleen non identify active>")
            print("<procedure: close all files>")
            self.close_game()

    def close_game(self):
        self.game_in_progress = False
        pygame.quit()
        quit()
