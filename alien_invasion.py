import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.bg_background = pygame.image.load('images/background.png')
        
         #Crea una instancia para guardar las estadísticas del juego
        self.stats = GameStats(self)  
        self.sb = Scoreboard(self)   
        
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  #Agrupamos las balas disparadas
        self.aliens = pygame.sprite.Group() 
        self._create_fleet()
        
       
        pygame.display.set_caption("Alien Invasion")
        
        #Inicia Alien Invasion con estado ACTIVO
        self.game_active = False
        
        #Crea el boton PLAY
        self.play_button = Button(self, "Play")
                
    def run_game(self): #==> Inicia el bucle principal del juego
        
        while True: 
            
            self._check_events()
            
            if self.game_active: 
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(60)
    
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            
            #Disminuye ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #Se deshace de los aliens y balas restantes
            self.aliens.empty()
            self.bullets.empty()
            #Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()
            #Pausa
            sleep(0.5)
            
            
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    
    def _update_bullets(self):
             #Se deshace de las balas que han desaparecido
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
                    
            self._check_bullet_alien_collisions() 
          
    def _check_bullet_alien_collisions(self):
        #Responde a las colisiones bala-alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions: 
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
            self.sb.prep_score()
            self.sb.check_high_score()
            
        #Si no hay aliens, se renueva la flota
        if not self.aliens:
                self.bullets.empty()
                self._create_fleet()  
                self.settings.increase_speed()
                
                #Aumenta el nivel
                self.stats.level += 1
                self.sb.prep_level()
                          
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        
        #Busca colisiones alien-nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        #Busca aliens llegando al fondo de la pantalla
        self._check_aliens_bottom()
     
    def _check_aliens_bottom(self):
        #Comprueba si algún alien llega al fondo de la pantalla
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Trata esto como si la nave hubiese sido alcanzada
                self._ship_hit()
                break
       
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 8 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
            
    def _check_fleet_edges(self):
        #Responde si algún alien ha llegado a un borde
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        #Baja toda la flota y cambia su direccion
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, x_position, y_position):
        #Crea un alien y lo coloca en la fila
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
               
    def _check_events(self):
        #Responde a pulsaciones de teclas y eventos de ratón
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    sys.exit()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                 self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
    def _check_play_button(self, mouse_pos):
        
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.game_active = True
            self.sb.prep_score()
            pygame.mouse.set_visible(False)
            
            #Reestablece estadísticas del juego
            self.stats.reset_stats()
            
            #Se deshace de los aliens y balas que quedan
            self.aliens.empty()
            self.bullets.empty()
            
            #Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()        
                           
    def _check_keydown_events(self, event):
        #Responde a pulsaciones de teclas
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()    
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False    
    
    def _fire_bullet(self):
        #Crea una nueva bala y la añade al grupo
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)            
                     
    def _update_screen(self):
        #Actualiza las imagenes en la pantalla y cambia a la pantalla nueva
            self.screen.blit(self.bg_background, (0,0))  #==> dibuja el background usando el fondo
                        
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            
            self.ship.blitme()
            
            self.aliens.draw(self.screen)
            
            self.sb.show_score()
            
            #Dibuja el boton para jugr si el juego está INACTIVO
            if not self.game_active:
                self.play_button.draw_button()
            pygame.display.update
            pygame.display.flip()
                        
if __name__ == '__main__':  # ==> Verifica si este script está siendo ejecutado como el programa principal
    
    ai = AlienInvasion() #==> Hace una instancia del juego y lo ejecuta
    ai.run_game()
    
    
#-------Controlar la tasa de frames--------
#Creamos un reloj y nos aseguramos que el segundero suene cada vez que pasa por el bucle principal. Siempre que el bucle procese más rápiddamente que la tasa que definamos, Pygame calculará la cantidad de tiempo correcta para hacer una pausa, con el objetivo de que el juego se ejecute siguiendo una tasa corriente

