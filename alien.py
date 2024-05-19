import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        #Carga la imagen del alien y configura su atributo rect
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        
        #Inicia un nuevo alien cerca de la parte superior izq de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #guarda la posicion  horizontal exacta dle alin
        self.x = float(self.rect.x)
        
    def update(self):
        #Mueve el alien a la derecha o izquierda
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        
    def check_edges(self):
        #Devuelve true si el alien está en el borde de la pantalla
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)