from Batalla_final.enemy2 import Enemy, Enemy2
import random

class SistemaOleada():
    def __init__(self):
        self.oleada_actual = 1              #Crea una variable que va ir contando el numero de oleadas 
        self.enemigos = []                  #Crea una lista de donde se van a ir cargando los enemigos
        
        

    #Genera los enemigos dependiendo de la cantidad 
    def generar_enemigo (self, cantidad):
       
        for i in range (cantidad):

            x = random.choice([0, 800])
            y = random.randint (50, 550)

            enemigo = Enemy(x, y, 30, 2)
            
            self.enemigos.append (enemigo)

        
    def generar_enemigo2 (self, cantidad):
        borde_derecho = 50
        borde_izquierdo= 850
        borde_superior = 200
        borde_inferior = 480   

        for i in range (cantidad):
        
            x = random.randint(borde_derecho,  borde_izquierdo)
            y = random.randint (borde_superior, borde_inferior)
            enemigo = Enemy2 (x, y, 50, 1)

            self.enemigos.append(enemigo)

    #Inicia la oleada y dependiendo de la oleada aumenta o cambia los enemigos 
    def iniciar_oleada (self):

        if self.oleada_actual ==1:
            self.generar_enemigo(4)

        elif self.oleada_actual == 2:
            self.generar_enemigo2 (3)

        elif self.oleada_actual == 3:
            for i in range(6):
                x = random.choice([-50, 800])
                y = random.randint (50, 550)

                tipo = random.choice ([1, 2])

                if tipo == 1:
                    enemigo = Enemy(x, y, 30, 2)
                
                else:
                    enemigo= Enemy2 (x, y, 50, 1)
                                
                self.enemigos.append (enemigo)

    #Detecta si ya no hay enemigos entonces para la oleada 
    def fin_oleada (self):

        if len(self.enemigos)==0:
            if self.oleada_actual<3 :

                self.oleada_actual += 1

                self.iniciar_oleada()    
            else:
                print ("Oleada completada")
