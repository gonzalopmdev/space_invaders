import pygame.font  #Permite mostrar texto en pantalla

class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        #Configura las dimensiones y propiedades del botón
        self.width, self.height = 220, 90
        self.button_color = (72,61,139)
        self.text_color = (252, 247, 94)
        self.font = pygame.font.SysFont("impact", 60)
        
        #Crea el objeto RECT del botón y lo centra
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        #Solo hay que preparar el mensaje del botón una vez
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        #Convierte msg en una imagen renderizada y centra el texto en el botón
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        #Dibuja un botón en blanco y luego dibuja el mensaje
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)