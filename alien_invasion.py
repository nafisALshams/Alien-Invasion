import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """The class which will manage all game assets and behavior."""
    def __init__(self):
        """Initializing the game and creating game resources."""
        pygame.init()
        #creating an instance for settings class from settings module
        self.settings = Settings()

        #setting up the primary screen resolution or window size
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        #setting the title of  the window
        pygame.display.set_caption("Alien Invasion")

        #create an instance to store game statistics.
        #and creating an instance of scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        #create an instance for ship
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Setting the clock to make the game run consistently
        self.clock = pygame.time.Clock()

        #start the game in an active state.
        self.game_active = False

        #Making the play button by creating an instance
        self.play_button = Button(self, "Play")


    def run_game(self):
        """The main loop for the game will start here."""
        while True:
            #sending the keypress and event loop to the helper method
            self._check_events()

            if self.game_active:
                self.bullets.update()
                self.ship.update()

                #helper method to update and remove old bullets
                self._update_bullets()

                #helper method to update aliens position
                self._update_aliens()

            #helper method to redraw the screen
            self._update_screen()

            # Setting the frame rate
            self.clock.tick(165)


    def _check_aliens_bottom(self):
        """Check if any aliens hit the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #the same outcome as the ship getting hit
                self._ship_hit()
                break


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:

            #decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #getting rid of remaining bullets and aliens after hit.
            self.bullets.empty()
            self.aliens.empty()

            #create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause the game to show collision
            sleep(0.5)
        else:
            self.game_active = False
            #making the mouse visible again
            pygame.mouse.set_visible(True)


    def _update_bullets(self):
        """Update position  of bullets and get rid of old bullets"""
        #update bullet positions.
        self.bullets.update()

        # getting rid of bullets that reach the top
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to any bullet alien collision"""
        # check for any bullets that has hit an alien rect
        # if so, then get rid of the bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        #checking collisions and adding a point  if hit.
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        # checking if there are aliens left
        if not self.aliens:
            # destroy all bullets and create the new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #incease level.
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """ Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        #looking for alien and ship collisions.
        if pygame.sprite.spritecollide(self.ship, self.aliens, False):
            self._ship_hit()

        #looking for aliens hitting bottom of the screen.
        self._check_aliens_bottom()


    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Create an alien and keep adding aliens until there's  no room left.
        #spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 8 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            #finished a row; reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet"""
        #making individual alien
        # alien = Alien(self)
        # self.aliens.add(alien)
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """Respond if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1



    def _update_screen(self):
        """update images on the screen and flip to the new screen"""
        # Re-drawing the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet  in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        #Draw the score information.
        self.sb.show_score()

        #Draw the play button if game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


    def _check_events(self):
        """Responds to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            #keydown for starting continuous movement
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)


            # keyup for stopping continuous movement
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            #mousebuttondown for starting to play in the mouse pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)



    def _check_play_button(self, mouse_pos):
        """Start a new game when the play button is clicked"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #reset the game settings first then restart
            self.settings.initialize_dynamic_settings()
            self._start_game()



    def _start_game(self):
        """Starting the game if conditions met"""
        # Reset the game Stats.
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True  # The game starts again

        # getting rid of any bullets and aliens
        self.bullets.empty()
        self.aliens.empty()

        # create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # hiding mouse pointer.
        pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            # ship moves right
            self.ship.moving_right += True


        elif event.key == pygame.K_LEFT:
            # ship moves left
            self.ship.moving_left = True

        elif event.key == pygame.K_ESCAPE:
            #pressing esc key to quit the game
            sys.exit()


        elif event.key == pygame.K_SPACE:
            #pressing space to fire a bullet
            self._fire_bullet()

        elif event.key == pygame.K_p:
            #pressing p to start the game
            self._start_game()


    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            # ship stops moving right
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            # ship stops moving left
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


"""Driver code"""
#Make a game instance and run the game.
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()


