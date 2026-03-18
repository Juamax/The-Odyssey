import pygame
import random
from Batalla_final.entidad2 import Entidad


class Enemy(Entidad):

    def __init__(self, x, y, vida, velocidad):
        super().__init__(x, y, vida, velocidad)

        #Hitbox- al pecho aproximado
        self.rect = pygame.Rect(0, 0, 65, 60)
        self.rect.center =(x, y)

        #Animaciones 
        self.move_frames = self.cargar_frames ("Batalla_final/animacion/enemigo1/enemigo_final1_mover.png")
        self.atacar_frames = self.cargar_frames ("Batalla_final/animacion/enemigo1/enemigo_final1_atacar.png")
        self.muerte_frames = self.cargar_frames ("Batalla_final/animacion/enemigo1/enemigo_final1_muerte.png")
        
        #ESTADOS DEL PERSONAJE
        self.estado = "move"
        self.frame_index = 0
        self.velocidad_animacion = 0.1
        self.direccion = "derecha"

        self.tiempo_ataque = 0
        self.muerto = False


    def cargar_frames (self, ruta):
        sprite_sheet = pygame.image.load (ruta).convert_alpha()

        frame_ancho = 1650 // 3
        frame_alto = 448

        frames= []

        for i in range(3):
            frame = sprite_sheet.subsurface((i * frame_ancho, 0, frame_ancho, frame_alto))
            #SIrve para reescalar la escala de los enemigos
            frame = pygame.transform.scale (frame, (200, 120))
            frames.append (frame)

        return frames


    def move(self, player):

        if self.muerto :
            return
        
        if self.estado == "atacar":

            if self.frame_index< 2:
                return
            
            else:
                self.estado ="move"

        self.estado ="move"

        distancia_x = player.x - self.x
        distancia_y = player.y - self.y


        if distancia_x >0:
            self.direccion = "derecha"
        else:
            self.direccion = "izquierda"

        if distancia_x > 0:
            self.x += self.velocidad
        else:
            self.x -= self.velocidad

        if distancia_y > 0:
            self.y += self.velocidad
        else:
            self.y -= self.velocidad

        self.rect.center = (self.x, self.y)


    def attack(self, player):
        if self.muerto:
            return
        
        tiempo = pygame.time.get_ticks()

        if tiempo - self.tiempo_ataque > 2000:

            self.estado = "atacar"
            self.frame_index = 0

            area_ataque = pygame.Rect( self.rect.centerx-30, self.rect.centery-20, 60, 40)

            if area_ataque.colliderect(player.rect):
                player.daño_recibido(10)

            self.tiempo_ataque = tiempo


    def daño_recibido(self, damage, player):

        if self.muerto:
            return

        self.vida -= damage

        if self.x > player.x:
            self.x += 40

        else:
            self.x -= 40

        self.y += random.randint(-5,5)

        self.rect.center = (self.x, self.y)

        if self.vida <= 0:
            self.estado = "muerto"
            self.frame_index= 0
            self.muerto = True


    def animar (self):


        if self.estado == "muerto":
            self.frame_index += 0.08

            if self.frame_index >= len(self.muerte_frames):
                self.frame_index = len(self.muerte_frames) - 1

            return
        
        self.frame_index += self.velocidad_animacion
        
        if self.frame_index>= len(self.move_frames):
            self.frame_index=0


    def draw(self, screen):
        

        self.animar()
        
        #ESTADO DEL ENEMIGO
        if self.estado == "move":
            image= self.move_frames[int (self.frame_index)]

        elif self.estado == "atacar":
            image= self.atacar_frames[int (self.frame_index)]

        elif self.estado =="muerto":
            image = self.muerte_frames [int (self.frame_index)]

        #DIRECCION DEL  ENEMIGO
        if self.direccion == "izquierda":
            image = pygame.transform.flip (image, True, False)

        #POSICION DEL ENEMIGO
        rect_imagen = image.get_rect(center=self.rect.center)
        screen.blit(image, rect_imagen)




    def separar_enemigo(self, enemigos):

        for enemigo in enemigos:

            if enemigo != self:

                distancia_x = self.x - enemigo.x
                distancia_y = self.y - enemigo.y

                distancia= (distancia_x**2 + distancia_y**2) **0.5

                if abs(distancia) < 40 and abs(distancia_y) != 0:

                    fuerza = 2 

                    self.x += (distancia_x/distancia)*fuerza
                    self.y += (distancia_y/distancia)*fuerza

        self.rect.center = (self.x, self.y)


class Enemy2 (Enemy):
    def __init__(self, x, y, vida, velocidad):
        super().__init__(x, y, vida, velocidad)

        self.rect = pygame.Rect (0, 0, 80, 70)
        self.rect.center = (x, y)

        #Animaciones 
        self.move_frames = self.cargar_frames ("Batalla_final/animacion/enemigo2/enemigo2_final_mover.png")
        self.atacar_frames = self.cargar_frames ("Batalla_final/animacion/enemigo2/enemigo2_final_atacar.png")
        self.muerte_frames = self.cargar_frames ("Batalla_final/animacion/enemigo2/enemigo2_final_muerte.png")
                
        #ESTADOS DEL PERSONAJE
        self.estado = "move"

        self.tiempo_ataque = 0
        self.frame_index = 0
        self.velocidad_animacion = 0.1
        self.muerto = False

    def cargar_frames (self, ruta):
        sprite_sheet = pygame.image.load (ruta).convert_alpha()

        frame_ancho = 1650 // 3
        frame_alto = 448

        frames= []

        for i in range(3):
            frame = sprite_sheet.subsurface((i * frame_ancho, 0, frame_ancho, frame_alto))
            #SIrve para reescalar la escala de los enemigos
            frame = pygame.transform.scale (frame, (240, 150))
            frames.append (frame)

        return frames
    

    def attack(self, player):
        if self.muerto:
            return
        
        tiempo = pygame.time.get_ticks()

        if tiempo - self.tiempo_ataque > 2500:

            self.estado = "atacar"
            self.frame_index = 0

            area_ataque = pygame.Rect( self.rect.centerx-30, self.rect.centery-20, 60, 40)

            if area_ataque.colliderect(player.rect):
                player.daño_recibido(20)

            self.tiempo_ataque = tiempo


    def daño_recibido(self, damage, player):

        if self.muerto:
            return

        self.vida -= damage

        if self.x > player.x:
            self.x += 20

        else:
            self.x -= 20

        self.y += random.randint(-5,5)

        self.rect.center = (self.x, self.y)

        if self.vida <= 0:
            self.estado = "muerto"
            self.frame_index= 0
            self.muerto = True  
    

    def animar (self):

        self.frame_index += self.velocidad_animacion
        
        if self.estado == "muerto":
            self.frame_index += 0.03

            if self.frame_index >= len(self.muerte_frames):
                self.frame_index = len(self.muerte_frames) - 1

            return
        
        if self.frame_index>= 3:
            self.frame_index=0
        

    def draw(self, screen):

        self.animar()


        if self.estado == "move":
            image= self.move_frames[int (self.frame_index)]

        elif self.estado == "atacar":
            image= self.atacar_frames[int (self.frame_index)]

        elif self.estado =="muerto":
            image = self.muerte_frames [int (self.frame_index)]

        if self.direccion == "izquierda":
            image = pygame.transform.flip (image, True, False)

        rect_image = image.get_rect(center = self.rect.center)
        screen.blit(image, rect_image)

    
    def separar_enemigo(self, enemigos):

        for enemigo in enemigos:

            if enemigo != self:

                distancia_x = self.x - enemigo.x
                distancia_y = self.y - enemigo.y

                if abs(distancia_x) < 40 and abs(distancia_y) < 40:

                    if distancia_x > 0:
                        self.x += 2

                    else:
                        self.x -= 2

                    if distancia_y < 0:
                        self.y += 2

                    else:
                        self.y -= 2

        self.rect.center = (self.x, self.y)


