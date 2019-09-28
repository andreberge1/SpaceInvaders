import pygame
from settings import Settings

class Menu:
    """Class to create the game menu start/pause menu."""

    def __init__(self, ai_game):
        """Initialize main menu."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.settings = Settings()

        # Set the dimensions and properties of each button
        self.width, self.height = 384, 100
        self.button_color = self.settings.button_color
        self.text_color = self.settings.text_color
        self.button_font = self.settings.button_font
        self.menu_font = self.settings.menu_font

        # Creating the header for the menu.
        self.menu_text = self.menu_font.render('Alien Invasion', True, 
                    self.settings.white_color, self.settings.bg_color)
        self.menu_text_rect = self.menu_text.get_rect()
        self.menu_text_rect.midtop = (self.settings.screen_width // 2,
                                        50)
        
        # Store placement of buttons
        self.play_rect = pygame.Rect(768, 500,
                                                self.width, self.height)
        self.restart_rect = pygame.Rect(768, 650,
                                                self.width, self.height)
        self.quit_rect = pygame.Rect(768, 800,
                                                self.width, self.height)

        # Store text values and center text on the button
        self.text_play = self.button_font.render(
            'Play', True, self.text_color, self.button_color)
        self.text_play_rect = self.text_play.get_rect()
        self.text_play_rect.center = self.play_rect.center


        self.text_restart = self.button_font.render(
            'Restart', True, self.text_color, self.button_color)
        self.text_restart_rect = self.text_restart.get_rect()
        self.text_restart_rect.center = self.restart_rect.center


        self.text_quit = self.button_font.render(
            'Quit', True, self.text_color, self.button_color)
        self.text_quit_rect = self.text_quit.get_rect()
        self.text_quit_rect.center = self.quit_rect.center

        self.buttons = [
        [self.text_play, self.text_play_rect],
        [self.text_restart, self.text_restart_rect],
        [self.text_quit, self.text_quit_rect]
        ]

    def draw_menu(self):
        self.screen.blit(self.menu_text, self.menu_text_rect)

        self.screen.fill(self.button_color, self.play_rect)
        self.screen.blit(self.text_play, self.text_play_rect)

        self.screen.fill(self.button_color, self.restart_rect)
        self.screen.blit(self.text_restart, self.text_restart_rect)

        self.screen.fill(self.button_color, self.quit_rect)
        self.screen.blit(self.text_quit, self.text_quit_rect)