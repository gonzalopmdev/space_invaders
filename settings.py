import pygame

class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_background = pygame.image.load('images/background.png')
        self.bg_color = (255, 255, 255)
        self.bg_sb_color = (30, 30, 30)
        
        #Stats config
        self.ship_limit = 3
        
        #Config balas
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,255,0)
        self.bullets_allowed = 3
        
        #Config alien
        self.fleet_drop_speed = 10
        
        #Rapidez con que se acelera el juego
        self.speedup_scale = 1.1
        
        #Lo rápido que aumenta el valor en puntos de los aliens
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0    
        
        #fleet_direction de 1 representa derecha y -1 izquierda
        self.fleet_direction = 1
        
        #Configuracion de puntuacion
        self.alien_points = 50
        
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)