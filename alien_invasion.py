import sys
import pygame
from settings import Settings


class AlienInvasion:
    """The class which will manage all game assets and behavior."""
    def __init__(self):
        """Initializing the game and creating game resources."""
        pygame.init()
        #creating an instance for settings class from settings module
        self.settings = Settings()

        #setting up the primary screen resolution or window size
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        #setting the title of  the window
        pygame.display.set_caption("Alien Invasion")

        #Setting the clock to make the game run consistently
        self.clock = pygame.time.Clock()




    def run_game(self):
        """The main loop for the game will start here."""
        while True:
            #Watching the keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            #Re-drawing the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)

            #Making the most recent drawn screen visible.
            pygame.display.flip()
            #Setting the frame rate
            self.clock.tick(60)


"""Driver code"""
#Make a game instance and run the game.
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()


