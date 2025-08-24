class Settings:
    """A class to store all settings for the game"""
    def __init__(self):
        """Initializing the game's settings"""

        #screen settings
        self.screen_width = 1200
        self.screen_height = 800

        #setting the background color in RGB format
        self.bg_color = (230,230,230)

        #for the ship's movement speed
        self.ship_speed = 1.5
