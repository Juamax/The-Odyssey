import pygame
from Odysseus.entidad import Entidad
#Clase que representa al personaje jugable del juego 
class Player (Entidad):
    
    #Constructor 
    def __init__(self, x, y, vida, velocidad):
        super().__init__(x, y, vida, velocidad)

        #hitbox
        self.rect= pygame.Rect (0, 0 , 70, 80)
        self.rect.center =(x, y)

        #tiempos
        self.tiempo_ataque = 0          #Tiempo para volver a atacar
        self.tiempo_esquivar = 0        # Tiempo para volver a esquivar
        
        #Invulnerabilidad
        self.invulnerabilidad =False    # Esto controla si el jugador puede recibir danho 
        self.tiempo_invul= 0            # Tiempo que dura la invulnerabilidad 

        #Direccion
        self.direccion = "derecha"

        #ANIMACIONES
        self.move_frames= self.cargar_frames ("Odysseus/animacion/personaje/personaje_movimiento.png")
        self.atacar_frames =self.cargar_frames ("Odysseus/animacion/personaje/personaje_atacar.png")
        self.esquivar_frames =self.cargar_frames ("Odysseus/animacion/personaje/personaje_esquivar.png")
        self.morir_frames= self.cargar_frames ("Odysseus/animacion/personaje/personaje_muerte.png")

        #Estados
        self.estado = "move"
        self.frame_index = 0
        self.velocidad_animacion = 0.1

        #
        self.atacando = False
        self.esquivando = False
        self.muerto = False

        #Limites de pantalla 
        self.borde_derecho = 50
        self.borde_izquierdo= 850
        self.borde_superior = 250
        self.borde_inferior = 500

        #BARRA VIDA
        self.barra_imagen = pygame.image.load ("Odysseus/animacion/barra_vida/vida.png").convert_alpha()
        self.barra_x = 70
        self.barra_y = 24
        self.barra_ancho = 214
        self.barra_alto = 32
        self.vida_max = vida
        self.vida_visible = vida

    def animar(self):
        
        if self.estado == "muerto":
            self.frame_index += 0.05

            if self.frame_index>= len (self.morir_frames):
                self.frame_index = len(self.morir_frames)-1

            return

        if self.estado == "atacar":
            self.frame_index += 0.2
            
            if self.frame_index>= len (self.atacar_frames):
                self.frame_index = 0
                self.estado = "move"
                self.atacando = False
            return

        if self.estado == "esquivar":
            self.frame_index += 0.15

            if self.frame_index >= len(self.esquivar_frames):
                self.frame_index = 0
                self.estado = "move"
                self.esquivando = False

            return
        
        if self.estado == "move":
            self.frame_index += 0.1

            if self.frame_index>=len (self.move_frames):
                self.frame_index = 0

    def cargar_frames (self, ruta):
        sprite_sheet = pygame.image.load (ruta).convert_alpha()

        frame_ancho = 1650 // 3
        frame_alto = 448

        frames= []

        for i in range(3):
            frame = sprite_sheet.subsurface((i * frame_ancho, 0, frame_ancho, frame_alto))
            #SIrve para reescalar la escala de los enemigos
            frame = pygame.transform.scale (frame, (180, 120))
            frames.append (frame)

        return frames

    #Metodo o funcion que puede realizar el personaje 
    def move (self, teclas):
        if self.muerto:
            return


        #teclas = pygame.key.get_pressed()   #Devuelve una lista de teclas que se presionan  
        if self.estado in ["atacar", "esquivar", "muerto"]:
            return
        

        if teclas[pygame.K_w]:             #Funcion arriba: Pregunta si es que la tecla w es presionada si si entonces devuelve True 
            self.y -= self.velocidad
        
        if teclas[pygame.K_s]:             #Funcion abajo
            self.y += self.velocidad
        
        if teclas[pygame.K_a]:             #Funcion izquierda
            self.x -= self.velocidad
            self.direccion = "izquierda"

        if teclas[pygame.K_d]:             #Funcion derecha
            self.x += self.velocidad
            self.direccion = "derecha"
        
        #Limita el movimiento del jugador para que no salga de la pantalla 
        self.x = max (self.borde_derecho, min(self.x, self.borde_izquierdo))
        self.y = max (self.borde_superior, min(self.y, self.borde_inferior))


        self.rect.center =(self.x, self.y) #Decimos que el rectangulo del jugador estara en la posicion x e y 
        
        if teclas[pygame.K_w] or teclas[pygame.K_s] or teclas[pygame.K_d] or teclas[pygame.K_a]:
            self.estado ="move"

    #  Dibujaremos al personaje dentro de la pantalla 
    def draw (self, screen):
        self.animar()

        #analiza el estado de la variable para asignar una animacion 
        if self.estado == "move":
            image = self.move_frames [int (self.frame_index)]

        elif self.estado== "atacar":
            image = self.atacar_frames [int (self.frame_index)]

        elif self.estado == "esquivar":
            image = self.esquivar_frames[int(self.frame_index)]

        elif self.estado == "muerto":
            image = self.morir_frames [int(self.frame_index)]

        if self.direccion == "izquierda":
            image = pygame.transform.flip (image, True, False)
        
        rect_image = image.get_rect (center = self.rect.center)
        screen.blit(image, rect_image)

    # Ejecuta un ataque rapido pero con menos danho
    def ataque_rapido (self, enemigos:Entidad ):
        tiempo = pygame.time.get_ticks ()

        if tiempo - self.tiempo_ataque > 150:
            alto = 10
            ancho = 15
            self.estado = "atacar"
            self.frame_index = 0

            if self.direccion == "derecha":
                area_ataque = pygame.Rect(self.rect.centerx +10, self.rect.centery - alto //2 , ancho, alto) #Golpea hacia la derecha 
            
            else:
                area_ataque = pygame.Rect (self.rect.centerx - 10 - ancho, self.rect.centery - alto//2, ancho, alto) #Golpea hacia la izquierda
                #Los valores que se le restan seria para poder centrar el hit-box y no quede fguera del personaje 

            for enemigo in enemigos:
                if area_ataque.colliderect (enemigo.rect): #Si el enemigo esta en el rango de ataque entonces le baja la vida
                    enemigo.daño_recibido (5, self)
            
            self.tiempo_ataque = tiempo

    #Ejecuta el ataque fuerte 
    def ataque_fuerte (self, enemigos):
        tiempo= pygame.time.get_ticks () # Devuelve el tiempo desde que comenzo el juego

        if tiempo - self.tiempo_ataque > 250:
            ancho = 20
            alto = 25

            self.estado = "atacar"
            self.frame_index = 0 

            if self.direccion == "derecha":
                area_ataque = pygame.Rect(self.rect.centerx + 12, self.rect.centery - alto // 2, ancho, alto) 

            else:
                area_ataque = pygame.Rect (self.rect.left - 25 - ancho, self.rect.centery - alto //2, ancho, alto)

            for enemigo in enemigos :
                
                if area_ataque.colliderect (enemigo.rect):
                    enemigo.daño_recibido (15, self)
            
            self.tiempo_ataque = tiempo

    #Con esta funcion podemos esquivar hcaia adelante a los enemigos 
    def esquivar (self):
        tiempo =pygame.time.get_ticks ()  

        if tiempo - self.tiempo_esquivar > 2000: #Esto permite que el jugador use cada 2 segundos esta habilidad 

            self.estado = "esquivar"
            self.frame_index=0
            
            distancia_esquivar = 100

            #Usamos esta funcion para poder esquivar cuando este mirando hacia la derecha 
            if self.direccion == "derecha":
                self.x += distancia_esquivar
            
            #Si no esta mirando hacia la derecha entonces esquiva hacia la izquierda
            else:
                self.x -= distancia_esquivar

            self.x = max (20, min(self.x, 780))  #Creamos los limites para que no salga de la pantalla 
            self.rect.center = (self.x, self.y)  #Actualizamos la posicion 

            self.invulnerabilidad = True         #Activar vulnerabilidad
            self.tiempo_invul = tiempo           #tiempo que dura la "invisibilidad"

            self.tiempo_esquivar = tiempo        #Guarda el tiempo en el que se uso la habilidad 

    #Con esta funcion decimos cuanto tiempo no podra recibir danho 
    def temp_invul (self):
        if self.invulnerabilidad:                   #Si es True entra a la funcion
             
             tiempo = pygame.time.get_ticks()   
             if tiempo - self.tiempo_invul > 1000:   #SI vulnerabilidad paso los 0,5 segundo se desactiva 
                self.invulnerabilidad = False
    
    #Recibira danho solo si no esta esquivando o invulnerabilidad no esta activo
    def daño_recibido(self, damage):
        if self.invulnerabilidad or self.muerto:
            return
        
        self.vida -=damage

        if self.vida <= 0:
            self.estado = "muerto"
            self.frame_index = 0
            self.muerto = True

        
    def barra_vida (self, screen):
        x=10
        y=5

        offset_x =75
        offset_y = 31
        ancho = 214
        alto =32

        if self.vida_visible > self.vida:
            self.vida_visible -= 0.5
        else:
            self.vida_visible = self.vida

        #PORCENTAJE de vida
        porcentaje = self.vida_visible / self.vida_max
        ancho_visible = int (ancho* porcentaje)

        #color de la vida 
        if porcentaje>0.6:
            color = (0, 200, 0)
        elif porcentaje> 0.3:
            color=(255, 165, 0)
        else:
            color =(200, 0, 0)

        #rellenar vida

        #fondo (vida perdida)
        pygame.draw.rect (screen, color, (x + offset_x, 
                                          y + offset_y,
                                          ancho_visible,
                                          alto))
        
        screen.blit (self.barra_imagen, (x, y))

