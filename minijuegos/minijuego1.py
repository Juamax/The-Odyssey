import pygame
from Odysseus.personaje import Player
from Odysseus.sistemaOleada import SistemaOleada
from Odysseus.entidad import Fondo


def ejecutar_minijuego1():

    pygame.init()

    ANCHO = 900
    ALTO = 550

    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("La Odisea - Beat'em Up")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 40)

    # imagen para fondo
    fondo = Fondo("Odysseus/animacion/fondo/fondo_2.png", ANCHO, ALTO)

    # Player
    player = Player(400, 300, 100, 5)

    # Enemigos
    oleadas = SistemaOleada()
    oleadas.iniciar_oleada()

    
    while True:

        clock.tick(60)

        fondo.draw(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_j:
                    player.ataque_rapido(oleadas.enemigos)

                if event.key == pygame.K_k:
                    player.ataque_fuerte(oleadas.enemigos)

                if event.key == pygame.K_l:
                    player.esquivar()

        teclas = pygame.key.get_pressed()

        player.move(teclas)
        player.temp_invul()

        player.draw(screen)
        player.barra_vida(screen)

        # Enemigos
        for enemigo in oleadas.enemigos[:]:

            enemigo.separar_enemigo(oleadas.enemigos)
            enemigo.move(player)
            enemigo.attack(player)

            enemigo.draw(screen)

            if enemigo.estado == "muerto" and enemigo.frame_index >= len(enemigo.muerte_frames) - 1:
                oleadas.enemigos.remove(enemigo)

        oleadas.fin_oleada()

        # CONDICIÓN DE VICTORIA
        if len(oleadas.enemigos) == 0:
            pygame.display.update()
            pygame.time.delay(1000)
            return "victoria"

        #GAME OVER
        if player.vida <= 0:

            texto = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(texto, (300, 280))

            pygame.display.update()
            pygame.time.delay(3000)

            return "derrota"

        pygame.display.update()



if __name__ == "__main__":

    def main():
        estado = ejecutar_minijuego1()

        if estado == "victoria":
            print("Ganaste")

        elif estado == "derrota":
            print("Perdiste")

        elif estado == "salir":
            print("Saliste del juego")


    main()