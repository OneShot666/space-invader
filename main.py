from random import randint
from src.asteroid_belt import AsteroidBelt
from src.sounds import SoundManager
from src.dialog import DialogBox
from src.player import Player
from src.vars import *
import asyncio
import pygame


# [v0.0.6] Allow to left click to shoot + mouse moving option + nb max of asteroids
# [v0.0.7] Add feedback + remove prints + put score behind player & belt
# [v0.0.8] . Add levels + level manager + shield (right click -> cost energy)
# [v0.0.9] ! Add death screen + go back to main menu
# [v0.1.0] L Add upgrades for spaceship & asteroids
class Game:
    def __init__(self):
        pygame.init()
        # Project data
        self.name = "Space Invader"
        self.creator = "One Shot"
        self.version = "v0.0.7"
        self.birthday = "19/11/2022"
        # Bool data
        self.first_launch =     True
        self.is_running =       True
        self.menu_in_progress = True
        self.lvl1_in_progress = False                                           # L Replace by current_level
        self.lvl2_in_progress = False
        self.lvl3_in_progress = False
        self.music_on =         True
        # Game data
        self.clock = pygame.time.Clock()
        self.fps = 60
        # Screen data
        self.bg_image =     None
        self.screen =       None
        self.screen_size =  None
        self.banner =       None
        self.banner_rect =  None
        self.banner_size =  None
        # Buttons data
        self.play_button =          None
        self.play_button_rect =     None
        self.play_button_size =     None
        # self.select_button =        None
        # self.select_button_rect =   None
        # self.select_button_size =   None
        # Gameplay data
        self.pressed = {}
        self.Players = pygame.sprite.Group()
        self.player = None
        # self.asteroids = pygame.sprite.Group()
        self.asteroid_belt = None
        self.score = 0
        # Font & Music data
        self.score_font =   None
        self.version_font = None
        self.font_color = (96, 96, 192)
        self.sound_manager = None
        self.song_name = "bg_music"                                             # Sound category
        self.dialogs_wait_list = []
        self.dialog = None
        # Screenshake data
        self.shake_duration = 0                                                 # In frames
        self.shake_intensity = 0                                                # In pixels
        self.offset = [0, 0]                                                    # Window offset

    def load_ressources(self):
        self.create_screen()
        self.create_banner()
        self.create_buttons()
        pygame.display.set_caption(game_name, ICON_NAME)                        # Set icon
        self.player = Player(self)
        self.Players.add(self.player)
        self.asteroid_belt = AsteroidBelt(self.screen_size, self.player)
        self.score_font =   pygame.font.Font(FONT_NAME, 50)
        self.version_font = pygame.font.Font(FONT_NAME, 20)
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
        self.banner_rect = self.banner.get_rect()
        self.banner_size = self.banner_rect[2:4]

    def create_buttons(self):
        play_button = pygame.image.load(PLAY_BUTTON_NAME)
        self.play_button = pygame.transform.scale(play_button, play_button_size)
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_size = self.play_button_rect[2:4]

        # Level selector data
        # level_select = pygame.image.load(LEVEL_SELECT_NAME)                   # L Not yet
        # self.select_button = pygame.transform.scale(level_select, level_select_size)
        # level_select_rect = self.select_button.get_rect()
        # self.select_button_size = level_select_rect[2:4]

    async def Run(self):
        await asyncio.sleep(1)

        self.load_ressources()
        await asyncio.sleep(0)

        print(f"Launching {game_name} [{self.version}] !")                      # ! Add text
        if self.first_launch and self.music_on:
            self.sound_manager.play_music(self.song_name, True)

        while self.is_running:
            self.calculate_shake()
            self.screen.blit(self.bg_image, self.offset)
            await self.inputs()

            if self.lvl1_in_progress:                                           # Levels in progress...
                self.update_game()
            elif self.lvl2_in_progress:
                self.update_game()
            elif self.lvl3_in_progress:
                self.update_game()
            else:
                self.display_main_menu()
            """ elif jeu.menu_in_progress:                                          # Sélection des niveaux
                for i in range(3):
                    level_select_rect.x = (taille_fenetre[0] * 0.5 - level_select_taille[0] * 0.5) // 1
                    level_select_rect.y = i * (taille_fenetre[1] * 0.1 + level_select_taille[1]) // 1
                    ecran.blit(level_select, level_select_rect)
                    lvl_text = jeu.font.render(f"Niveau {i + 1}", True, (0, 0, 0))  # Affiche les niveaux
                    ecran.blit(lvl_text, (level_select_rect.x * 0.5, level_select_rect.y * 0.5))  # Position du texte
            """

            pygame.display.flip()
            self.clock.tick(self.fps)
            await asyncio.sleep(0)

    async def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.pressed[event.key] = True

                if event.key == pygame.K_RETURN:
                    await self.launch_level()

                if event.key == pygame.K_ESCAPE:
                    self.close_game()                                           # L Replace by go to main menu

                if event.key == pygame.K_m:                                     # Toggle music
                    self.toggle_music()

            if event.type == pygame.KEYUP:                                      # Deactivate released keys
                self.pressed[event.key] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):
                    await self.launch_level()

            if event.type == pygame.QUIT:
                self.close_game()

    async def launch_level(self, level=1):                                      # Manage main menu
        if self.menu_in_progress:
            self.sound_manager.play_sound("launch")
            await asyncio.sleep(2)

            if not self.first_launch and self.music_on:
                self.sound_manager.play_music(self.song_name, True)

            self.menu_in_progress = False
            if level == 1:
                self.lvl1_in_progress = True
            elif level == 2:
                self.lvl2_in_progress = True
            elif level == 3:
                self.lvl3_in_progress = True
            else:
                self.menu_in_progress = True
            self.first_launch = False

    def display_main_menu(self):
        self.banner_rect.x = (self.screen_size[0] * 0.5 - self.banner_size[0] * 0.5) // 1
        self.banner_rect.y = (self.screen_size[1] * 0.35 - self.banner_size[1] * 0.5) // 1
        self.screen.blit(self.banner, self.banner_rect)
        self.play_button_rect.x = (self.screen_size[0] * 0.5 - self.play_button_size[0] * 0.5) // 1
        self.play_button_rect.y = (self.screen_size[1] * 0.45 + self.banner_size[1] * 0.5) // 1
        self.screen.blit(self.play_button, self.play_button_rect)

    def update_game(self):                                                      # Display game screen
        self.player.regen_energy()

        if self.player.is_following:
            self.player.follow_mouse()
        else:
            if self.pressed.get(pygame.K_UP) and self.player.rect.y > 0:            # Manage player movement
                self.player.move_up()
            elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y + self.player.rect.height < self.screen_size[1]:
                self.player.move_down()

            if self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
                self.player.move_left()
            elif self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < self.screen_size[0]:
                self.player.move_right()

        if self.pressed.get(pygame.K_SPACE) or pygame.mouse.get_pressed()[0]:
            self.player.shoot()
            self.pressed[pygame.K_SPACE] = False

        for rocket in self.player.Bullets:                                      # Manage player's bullets
            rocket.move()

        for asteroid in self.asteroid_belt.Asteroids:                           # Manage asteroids
            asteroid.fall()
            asteroid.update_flash()
            # asteroid.update_health_bar(self.screen)

        bullets_hits = self.check_bullet_collisions()                           # Manage collisions bullets-asteroid
        for rocket in bullets_hits:
            for asteroid in bullets_hits[rocket]:
                if asteroid.take_damage(self.player.rocket.damage):
                    self.start_shake(int(5 * asteroid.random), int(4 * asteroid.random))
                    self.sound_manager.play_sound("explosion")

        player_hits = self.check_collision(self.player, self.asteroid_belt.Asteroids, True)
        for asteroid in player_hits:                                            # Manage collisions player-asteroids
            self.sound_manager.play_sound("explosion")
            self.start_shake(int(15 * asteroid.random), int(12 * asteroid.random))
            self.player.hurt(asteroid.damage)

        # Draw everything in order
        version_text = self.version_font.render(f"{self.version}", True, self.font_color)
        self.screen.blit(version_text, (self.screen_size[0] * 0.92 + self.offset[0], self.screen_size[1] * 0.95 + self.offset[1]))
        score_text = self.score_font.render(f"S C O R E   {int(self.score)}", True, self.font_color)
        self.screen.blit(score_text, (self.screen_size[0] * 0.55 + self.offset[0], self.screen_size[1] * 0.15 + self.offset[1]))
        self.asteroid_belt.start_event()                                        # Create new asteroid
        self.asteroid_belt.draw(self.screen, self.offset)
        self.player.draw(self.screen, self.offset)
        self.player.update_health_bar(self.screen)
        self.player.update_energy_bar(self.screen)
        self.player.update_xp_bar(self.screen)
        self.screen.blit(self.player.image, (self.player.rect.x + self.offset[0], self.player.rect.y + self.offset[1]))

    def add_score(self, value=100):
        self.score += value

        if self.score < 0:
            self.score = 0

    def check_bullet_collisions(self):
        return pygame.sprite.groupcollide(self.player.Bullets, self.asteroid_belt.Asteroids,
            True, False, collided=pygame.sprite.collide_mask)

    @staticmethod
    def check_collision(sprite, group, kill=False):                             # Check group collide with another group
        return pygame.sprite.spritecollide(sprite, group, kill, pygame.sprite.collide_mask)

    def start_shake(self, duration=10, intensity=8):
        self.shake_duration = duration
        self.shake_intensity = intensity

    def calculate_shake(self):
        if self.shake_duration > 0:
            self.offset[0] = randint(-self.shake_intensity, self.shake_intensity)
            self.offset[1] = randint(-self.shake_intensity, self.shake_intensity)
            self.shake_duration -= 1
        else:
            self.offset = [0, 0]                                                # Reset shake

    def toggle_music(self):
        self.music_on = not self.music_on
        infinite = True if self.song_name == "bg_music" else False

        if self.music_on:
            self.sound_manager.play_music(self.song_name, infinite)             # L Add volume
        else:
            self.sound_manager.pause()

    def go_to_menu(self):
        self.menu_in_progress = True
        self.check_booleen()
        self.sound_manager.pause()

    def check_booleen(self):
        if self.menu_in_progress:
            self.lvl1_in_progress = False
            self.lvl2_in_progress = False
            self.lvl3_in_progress = False
        elif self.lvl1_in_progress:
            self.menu_in_progress = False
            self.lvl2_in_progress = False
            self.lvl3_in_progress = False
        elif self.lvl2_in_progress:
            self.menu_in_progress = False
            self.lvl1_in_progress = False
            self.lvl3_in_progress = False
        elif self.lvl3_in_progress:
            self.menu_in_progress = False
            self.lvl1_in_progress = False
            self.lvl2_in_progress = False

    def game_over(self):                                                  # Reset game
        self.sound_manager.play_sound("game_over")
        self.player.health = self.player.health_max
        self.player.energy = self.player.energy_max
        self.player.xp = 0
        self.player.xp_max = 100
        self.asteroid_belt.Asteroids = pygame.sprite.Group()
        self.score = 0

        self.go_to_menu()

    def close_game(self):
        self.is_running = False                                           # L Replace with death screen


async def start_game():
    game = Game()
    await game.Run()

if __name__ == "__main__":
    asyncio.run(start_game())
