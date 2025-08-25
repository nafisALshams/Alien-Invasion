class Settings:
    """A class to store all settings for the game"""
    def __init__(self):
        """Initializing the game's static settings"""

        #screen settings
        self.screen_width = 1200
        self.screen_height = 800

        #setting the background color in RGB format
        self.bg_color = (230,230,230)

        #ship settings that don't change
        self.ship_limit = 3

        #bullet settings that don't change
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 9

        #alien settings that don't change
        self.fleet_drop_speed = 10

        #how quickly the game will speed up
        self.speedup_scale = 1.1

        #how quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initializing settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        #scoring settings
        self.alien_points = 50


    def increase_speed(self):
        """Increased speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
