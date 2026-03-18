import pygame
#Clase Padre 
class Entidad:

    def __init__(self, x, y, vida, velocidad):

        self.x = x                               # Coordenada x del jugador
        self.y = y                               # Coordenada y del jugador

        self.velocidad = velocidad               # Velocidad base del los enemigos 

        self.vida = vida                         # Vida actual
        self.vida_max = vida                     #Disenho: Vida maxima del personaje

        #TAMANHO DEL PERONAJE O ENEMIGO
        self.ancho = 60
        self.alto = 60

        #HIT-BOX PRINCIPAL
        self.rect = pygame.Rect(0, 0, self.ancho, self.alto)
        self.rect.center=(x, y)

        #DIRECCION DE DONDE MIRA EL PERSONAJE
        self.direccion = "derecha" 

        #ESTADO GENERAL DEL PERSONAJE (Podria usarse para el tema de las animaciones)
        # Tipo camina, atacar, recibir golpes o idle que no este haciendo nada
        self.estado = "idle"
    
    def daño_recibido (self, damage):
        self.vida -= damage

class Fondo:

    def __init__(self, ruta, ancho, alto):
        self.imagen = pygame.image.load(ruta).convert()
        self.image = pygame.transform.scale(self.imagen, (ancho, alto))

    def draw (self, screen):
        screen.blit (self.imagen, (0, 0))        
