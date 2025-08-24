import pygame

class Ship:
    """The class which manages the user ship"""

    def __init__(self, ai_game):
        """Initialize the ship and setting the starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect  = ai_game.screen.get_rect()

        #load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()


        #start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        #store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)

        #movement flags; start with a ship which is stationary
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        #updating the self.x value not the self.rect.x
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Drawing the ship at its current location"""
        self.screen.blit(self.image, self.rect)

