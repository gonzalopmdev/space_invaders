class GameStats:
    #Sigue las estadisticas de Alien Invasion
    
    def __init__(self, ai_game):
        #Inicializa las stats
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0
        
    def reset_stats(self):
        #Inicializa las estadisticas que cambian durante el juego
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1