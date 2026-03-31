from random import randint
from src.asteroid_belt import AsteroidBelt
from src.level_card import LevelCard
from src.sounds import SoundManager
from src.dialog import DialogBox
from src.player import Player
from src.vars import *
import asyncio
import pygame
import sys


# [v0.0.6] Allow to left click to shoot + mouse moving option + nb max of asteroids
# [v0.0.7] Add feedback + remove prints + put score behind player & belt
# [v0.0.8] Add levels + level screen + use all spaceships & bullets & asteroids
# [v0.0.9] Add shield (right click -> cost energy) + comets + commands
# [v0.1.0] . Add retro mode + prepare for web (mouse follow pb, close function)
class Game:
    def __init__(self):
        pygame.init()
        # Project data
        self.name =     "Space Invader"
        self.creator =  "One Shot"
        self.version =  "v0.0.9"
        self.birthday = "19/11/2022"
        # Bool data
        self.is_web = sys.platform == "emscripten"
        self.first_launch =     True
        self.is_running =       True
        self.is_main_menu =     True
        self.is_selecting =     False
        self.is_music =         True
        # Game data
        if self.is_web:
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)   # Get web resolution
            try:
                from platform import window
                window.eval("document.addEventListener('contextmenu', e => e.preventDefault());")
            except: pass
        self.current_level = None
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
        self.select_button =        None
        self.select_button_rect =   None
        self.select_button_size =   None
        # Gameplay data
        self.pressed = {}
        self.LevelCards = []
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
        pygame.display.set_caption(self.name, ICON_NAME)                        # Set icon
        self.score_font =   pygame.font.Font(FONT_NAME, 50)
        self.version_font = pygame.font.Font(FONT_NAME, 20)
        self.create_screen()
        self.create_banner()
        self.create_buttons()
        self.create_level_cards()
        self.sound_manager = SoundManager()
        self.dialog = DialogBox()

    def create_screen(self):
        bg_image = pygame.image.load(BG_IMAGE_NAME)
        self.bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image_size = self.bg_image.get_rect()
        self.screen_size = bg_image_size[2:4]
        self.screen = pygame.display.set_mode(self.screen_size, pygame.SCALED)

    def create_banner(self):                                                    # Game icon on main menu
        banner = pygame.image.load(BANNER_NAME)
        self.banner = pygame.transform.scale(banner, banner_size)
        self.banner_rect = self.banner.get_rect()
        self.banner_size = self.banner_rect[2:4]

    def create_buttons(self):
        play_button = pygame.image.load(PLAY_BUTTON_NAME)
        self.play_button = pygame.transform.scale(play_button, play_button_size)
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_size = self.play_button_rect[2:4]

        level_select = pygame.image.load(LEVEL_SELECT_NAME)
        self.select_button = pygame.transform.scale(level_select, level_select_size)
        self.select_button_rect = self.select_button.get_rect()
        self.select_button_size = self.select_button_rect[2:4]

    def create_level_cards(self):
        self.LevelCards = []
        nb_level = 3
        card_width = int(self.screen_size[0] * 0.25)
        card_height = int(self.screen_size[1] * 0.7)
        spacing = 30

        total_width = (card_width * nb_level) + (spacing * (nb_level - 1))
        start_x = (self.screen_size[0] - total_width) // 2

        for i in range(nb_level):
            x = start_x + i * (card_width + spacing)
            y = int(self.screen_size[1] * 0.15)
            card = LevelCard(i + 1, x, y, card_width, card_height, LEVELS_DATA[i + 1], self.score_font)
            self.LevelCards.append(card)

    async def Run(self):
        await asyncio.sleep(1)

        self.load_ressources()
        await asyncio.sleep(0)

        if self.first_launch and self.is_music:
            self.sound_manager.play_music(self.song_name, True)

        while self.is_running:
            self.calculate_shake()
            self.screen.blit(self.bg_image, self.offset)
            await self.inputs()

            if self.current_level:
                self.update_game()
            elif self.is_selecting:
                self.display_select_menu()
            else:
                self.display_main_menu()

            pygame.display.flip()
            self.clock.tick(self.fps)
            await asyncio.sleep(0)

    async def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.pressed[event.key] = True

                if event.key == pygame.K_RETURN:
                    if self.is_main_menu:
                        self.is_main_menu = False
                        self.is_selecting = True

                if event.key == pygame.K_ESCAPE:
                    if not self.is_main_menu:
                        self.go_to_menu()
                    else:
                        self.close_game()

                if self.is_selecting:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        await self.launch_level(1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        await self.launch_level(2)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        await self.launch_level(3)

                if event.key == pygame.K_m:                                     # Toggle music
                    self.toggle_music()

                if self.current_level:
                    if event.key == pygame.K_s or event.key == pygame.K_b:
                        self.player.toggle_shield()

            if event.type == pygame.KEYUP:                                      # Deactivate released keys
                self.pressed[event.key] = False

            if self.is_selecting:
                await self.check_select_menu(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.is_main_menu and self.play_button_rect.collidepoint(event.pos):
                        self.is_main_menu = False
                        self.is_selecting = True
                if event.button == 3:
                    if self.current_level:
                        self.player.toggle_shield()

            if event.type == pygame.QUIT:
                self.close_game()

    async def launch_level(self, level=1):                                      # Manage main menu
        if self.is_selecting:
            self.sound_manager.play_sound("launch")
            await asyncio.sleep(0)

            if not self.first_launch and self.is_music:
                self.sound_manager.play_music(self.song_name, True)

            self.current_level = level
            self.is_selecting = False
            self.first_launch = False

            if self.current_level and self.current_level in LEVELS_DATA.keys():
                level_config = LEVELS_DATA[self.current_level]
                self.player = Player(self, level_config["player"], level_config["bullet"])
                self.asteroid_belt = AsteroidBelt(self.screen_size, self.player,
                    level_config["belt"], level_config["asteroid"], level_config["comet"])

    def get_web_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.is_web:
            surf = pygame.display.get_surface()
            if surf is None: return mx, my
            view_w, view_h = surf.get_size()
            rx = self.screen_size[0] / view_w
            ry = self.screen_size[1] / view_h
            return mouse_x * rx, mouse_y * ry
        return mouse_x, mouse_y

    def display_select_menu(self):                                              # Display level selection screen
        pos = self.get_web_mouse_pos()
        for card in self.LevelCards:
            if card.rect.collidepoint(pos):  # If mouse hover card
                pygame.draw.rect(self.screen, (255, 255, 255), card.rect, 3, border_radius=15)
            card.draw(self.screen)

    async def check_select_menu(self, event):                                   # Check if click on any level card
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for card in self.LevelCards:
                    if card.check_click(event.pos):
                        await self.launch_level(card.level_id)
                        return

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
            if self.pressed.get(pygame.K_UP) and self.player.rect.y > 0:        # Manage player movement
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
            # asteroid.update_health_bar(self.screen)                           # Hide for better immersion

        for comet in self.asteroid_belt.Comets:                                 # Manage comets
            comet.fall()
            comet.update_flash()
            # comet.update_health_bar(self.screen)                              # Hide for better immersion

        bullets_hits = self.check_bullet_collisions()                           # Manage collisions bullets-asteroid
        for rocket in bullets_hits:
            for asteroid in bullets_hits[rocket]:
                if asteroid.take_damage(self.player.rocket.damage):
                    self.start_shake(int(5 * asteroid.random), int(4 * asteroid.random))
                    self.sound_manager.play_sound("explosion")

        player_hits = self.check_collision(self.player, self.asteroid_belt.Asteroids, True)
        for asteroid in player_hits:                                        # Manage collisions player-asteroids
            if not self.player.is_shielding:
                self.sound_manager.play_sound("explosion")
                self.start_shake(int(15 * asteroid.random), int(12 * asteroid.random))
                self.player.hurt(asteroid.damage)
        comets_hits = self.check_collision(self.player, self.asteroid_belt.Comets, True)
        for comet in comets_hits:                                           # Manage collisions player-comets
            if not self.player.is_shielding:
                self.sound_manager.play_sound("explosion")
                self.start_shake(int(15 * comet.random), int(12 * comet.random))
                self.player.hurt(comet.damage)

        # Draw everything in order
        version_text = self.version_font.render(f"{self.version}", True, self.font_color)
        self.screen.blit(version_text, (self.screen_size[0] * 0.92 + self.offset[0], self.screen_size[1] * 0.95 + self.offset[1]))
        commands = f"[Left click / Space] Shoot\n[Right click / S / B] Shield\n[Mouse] Move"
        command_text = self.version_font.render(commands, True, self.font_color)
        self.screen.blit(command_text, (self.screen_size[0] * 0.01 + self.offset[0], self.screen_size[1] * 0.89 + self.offset[1]))
        score_text = self.score_font.render(f"S C O R E   {int(self.score)}", True, self.font_color)
        self.screen.blit(score_text, (self.screen_size[0] * 0.55 + self.offset[0], self.screen_size[1] * 0.15 + self.offset[1]))
        self.asteroid_belt.start_event()                                        # Create new asteroid
        self.asteroid_belt.draw(self.screen, self.offset)
        self.player.draw(self.screen, self.offset)

    def add_score(self, value=0):
        self.score = max(self.score + value, 0)

    def check_bullet_collisions(self):
        ast_hits = pygame.sprite.groupcollide(self.player.Bullets, self.asteroid_belt.Asteroids,
            True, False, collided=pygame.sprite.collide_mask)
        cmt_hits = pygame.sprite.groupcollide(self.player.Bullets, self.asteroid_belt.Comets,
            True, False, collided=pygame.sprite.collide_mask)
        ast_hits.update(cmt_hits)
        return ast_hits

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
        self.is_music = not self.is_music
        infinite = True if self.song_name == "bg_music" else False

        if self.is_music:
            self.sound_manager.play_music(self.song_name, infinite)             # L Add volume
        else:
            self.sound_manager.pause()

    def go_to_menu(self):
        self.is_main_menu = True
        self.current_level = None
        self.sound_manager.pause()

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
        self.sound_manager.pause()
        self.is_running = False


async def start_game():
    game = Game()
    await game.Run()

if __name__ == "__main__":
    asyncio.run(start_game())
