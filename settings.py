import pygame

class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings."""

        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1200
        self.bg_color = (0, 0, 0)

        # Color settings
        self.bullet_color = (57, 255, 20)
        self.text_color = (0, 0, 0)
        self.button_color = (141, 136, 136)
        self.white_color = (255, 255, 255)

        # Sound settings.
        self.soundtrack = pygame.mixer.Sound('sounds/soundtrack.wav')
        self.explosion = pygame.mixer.Sound('sounds/explosion.wav')
        self.game_over = pygame.mixer.Sound('sounds/game_over.wav')
        self.level_up = pygame.mixer.Sound('sounds/level_up.wav')
        self.shoot = pygame.mixer.Sound('sounds/shoot.wav')

        # Font settings
        self.menu_font = pygame.font.Font('images/Exo2.otf', 150)
        self.button_font = pygame.font.Font('images/Exo2.otf', 50)
        self.score_font = pygame.font.Font('images/Exo2.otf', 35)

        # Ship settings.
        self.ship_limit = 3


        # Bullet settings
        self.bullet_speed = 10
        self.bullet_height = 10
        self.bullet_width = 3
        self.bullet_allowed = 100

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up.
        self.speedup_scale = 1.1

        # How quickly the alien point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change during the game."""
        self.ship_speed = 5        
        self.alien_speed = 2.5
        self.fleet_direction = 1

        # Scoring.
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed sttings and lien point values."""
        self.ship_speed *= self.speedup_scale
        self.alien_speed *=self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)