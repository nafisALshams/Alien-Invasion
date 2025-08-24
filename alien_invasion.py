import sys
import pygame
from settings import Settings
from ship import Ship


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
        self.ship = Ship(self)

        #Setting the clock to make the game run consistently
        self.clock = pygame.time.Clock()




    def run_game(self):
        """The main loop for the game will start here."""
        while True:
            #sending the keypress and event loop to the helper method
            self._check_events()
            # Setting the frame rate
            self.clock.tick(165)
            #helper method to redraw the screen
            self._update_screen()

            self.ship.update()


            # Making the most recent drawn screen visible.


    def _update_screen(self):
        """update images on the screen and flip to the new screen"""
        # Re-drawing the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
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



    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            # ship stops moving right
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            # ship stops moving left
            self.ship.moving_left = False


"""Driver code"""
#Make a game instance and run the game.
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()


