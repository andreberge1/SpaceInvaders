#%%
import pygame
import sys
from time import sleep

from settings import Settings
from menu import Menu
from ship import Ship
from bullets import Bullets
from aliens import Alien
from game_stats import GameStats
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create behavior."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self. settings.screen_height),
                pygame.FULLSCREEN)

        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.menu = Menu(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = self.menu.buttons[0][1]
        self.restart_button = self.menu.buttons[1][1]
        self.quit_button = self.menu.buttons[2][1]

        self.pause_game = False 

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self.settings.soundtrack.play()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_button.collidepoint(mouse_pos):
                    self._check_play_button()
                elif self.restart_button.collidepoint(mouse_pos):
                    self._check_restart_button()
                elif self.quit_button.collidepoint(mouse_pos):
                    self._check_quit_button()

    def _check_play_button(self):
        """Play button with to different options for start and mid game."""
        if self.pause_game:
            # Activate game
            self.pause_game = False
            self.stats.game_active = True

            # Hide mouse coursor.
            pygame.mouse.set_visible(False)
        else:
            # Reset the game settings.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse coursor.
            pygame.mouse.set_visible(False)

    def _check_restart_button(self):
        """Button to restart the game."""
        # Reset the game settings.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ship()

        # Reset game statistics.
        self.pause_game = False

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide mouse coursor.
        pygame.mouse.set_visible(False)

    def _check_quit_button(self):
        sys.exit()

    def _check_keydown_events(self, event):
        """Respond to keydown presses."""
        if event.key == pygame.K_p:
            self.pause_game = True
            self.stats.game_active = False
            pygame.mouse.set_visible(True)  
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()

    def _check_keyup_events(self, event):
        """Respond to keyup events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullets(self):
        """Create a new bullet and at it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullets(self)
            self.bullets.add(new_bullet)
            pygame.mixer.Channel(1).play(self.settings.shoot)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        # Update bullet position.
        self.bullets.update()

        # Get rid of bullets that have dissapeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Resspond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.settings.soundtrack.stop()
            pygame.mixer.Channel(4).play(self.settings.level_up)
            self.bullets.empty()
            sleep(3)
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Creating an alien and fin the number og aliens in a row.
        # Spacing beteen each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit in the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
            (3 * alien_height) - ship_height * 4)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien an place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """
        Check if the fleet i at an edge,
            then update the position of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ship()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            self.settings.soundtrack.stop()
            pygame.mixer.Channel(2).play(self.settings.explosion)

            # Pause.
            sleep(2)

        else:
            self.settings.soundtrack.stop()
            pygame.mixer.Channel(2).play(self.settings.explosion)            
            pygame.mixer.Channel(3).play(self.settings.game_over)
            sleep(4)
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same way as if the ship got hit.
                self._ship_hit()
                break 

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        if self.stats.game_active == False:
            self.menu.draw_menu()
        else:
            self.ship.blitme()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.aliens.draw(self.screen)

            self.sb.show_score()

        if self.pause_game:
            self.menu.draw_menu()

        # Make the most reccently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()