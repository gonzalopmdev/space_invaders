import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        #Carga la imagen de la nave y obtiene su RECT
        self.image = pygame.image.load('images/ship_001.png')
        self.rect = self.image.get_rect()
        
        #Coloca cada nave nueva en el cntro de la parte inf de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom
        
        #Guarda un valor decimal para la posicion horizontal exacta de la nave
        self.x = float(self.rect.x)
        
        #Bandera de movimiento
        self.moving_right = False
        self.moving_left = False
        
    def blitme(self):
        
        #Dibuja la nave en su ubic actual
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        #Centra la nave en la pantalla
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        #actualiza el objeto rect de self.x
        self.rect.x = self.x
        
        