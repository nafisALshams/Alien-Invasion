class GameStats:
    """Track all the statistics for the game"""

    def __init__(self, ai_game):
        """Initializing the statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        #high score; should never be reset.
        self.high_score = 0


    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
