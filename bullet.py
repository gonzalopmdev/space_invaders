import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    
    #Clase para gestionar las balas disparadas desde la nave
    
    def __init__(self, ai_game):
       super().__init__()
       self.screen = ai_game.screen
       self.settings = ai_game.settings
       self.color = self.settings.bullet_color
       
       #Crea un rectángulo para la bala en (0,0) y luego establece la posición correcta.
       self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
       self.rect.midtop = ai_game.ship.rect.midtop
       
       #Guarda la posición de la bala como flotante
       self.y = float(self.rect.y) 
       
    def update(self):
        #Mueve la bala hacia arriba por la pantalla
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
        
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)