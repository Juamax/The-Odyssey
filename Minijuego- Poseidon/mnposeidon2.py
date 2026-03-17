import pygame
import random
from PIL import Image
# ꧁ ༺ ⚜ ༻ ꧂ VelvetProyect ꧁ ༺ ⚜ ༻ ꧂


class MiniJuego1:
    def __init__(self):
        self.ancho = 900
        self.alto = 550  # era 700
        self.fps = 60

        self.vida_jugador = 30
        self.vida_max = 30
        self.tiempo_supervivencia = 20

        self.color_fondo = (0, 0, 0)
        self.color_blanco = (255, 255, 255)

        # Paleta temática oceánica  ⋆౨ৎ˚⟡˖ 
        self.COLOR_AZUL      = (70, 170, 255)
        self.COLOR_AZUL_OSC  = (30, 90, 160)
        self.COLOR_CIAN      = (100, 220, 255)
        self.COLOR_ROJO      = (220, 50, 50)
        self.COLOR_VERDE     = (80, 220, 120)

    def dibujar_texto(self, pantalla, fuente, texto, x, y, color=(255, 255, 255)):
        superficie = fuente.render(texto, True, color)
        pantalla.blit(superficie, (x, y))

    def dibujar_texto_centrado(self, pantalla, fuente, texto, y, color=(255, 255, 255)):
        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect(center=(self.ancho // 2, y))
        pantalla.blit(superficie, rect)

    def dibujar_texto_con_sombra(self, pantalla, fuente, texto, x, y, color, sombra=(0, 0, 0)):
        sombra_surf = fuente.render(texto, True, sombra)
        pantalla.blit(sombra_surf, (x + 2, y + 2))
        surf = fuente.render(texto, True, color)
        pantalla.blit(surf, (x, y))

    def cargar_gif(self, ruta, escala=None):
        gif = Image.open(ruta)
        frames = []
        try:
            while True:
                frame = gif.convert("RGBA")
                datos = frame.tobytes()
                superficie = pygame.image.fromstring(datos, frame.size, frame.mode)
                if escala:
                    superficie = pygame.transform.scale(superficie, escala)
                frames.append(superficie)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        return frames

    def dibujar_barra(self, pantalla, x, y, ancho, alto, valor, maximo, color_lleno, color_vacio=(20, 40, 80), radio=6):
        ## ⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔ Barra / bordes. ⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔
        pygame.draw.rect(pantalla, color_vacio, (x, y, ancho, alto), border_radius=radio)
        fill_w = int(ancho * valor / maximo)
        if fill_w > 0:
            pygame.draw.rect(pantalla, color_lleno, (x, y, fill_w, alto), border_radius=radio)
        brillo = pygame.Surface((max(fill_w - 4, 0), alto // 3), pygame.SRCALPHA)
        brillo.fill((255, 255, 255, 60))
        pantalla.blit(brillo, (x + 2, y + 2))
        pygame.draw.rect(pantalla, (150, 210, 255), (x, y, ancho, alto), 2, border_radius=radio)

    def dibujar_panel_hud(self, pantalla, x, y, ancho, alto):
        ## Panel semi-transparente oscuro dorado.
        panel = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        panel.fill((5, 15, 40, 170))
        pantalla.blit(panel, (x, y))
        pygame.draw.rect(pantalla, self.COLOR_AZUL_OSC, (x, y, ancho, alto), 1, border_radius=8)

    def dibujar_borde_agua(self, pantalla, caja, tick):
        color_agua = (70, 170, 255)
        color_agua_claro = (180, 230, 255)

        pygame.draw.rect(pantalla, color_agua_claro, caja, 2)

        for i, x in enumerate(range(caja.left, caja.right, 30)):
            offset_y = int(3 * abs((tick // 3 + i) % 10 - 5))
            pygame.draw.arc(pantalla, color_agua, (x, caja.top - 5 - offset_y, 30, 15), 0, 3.14, 2)

        for i, x in enumerate(range(caja.left, caja.right, 30)):
            offset_y = int(3 * abs((tick // 3 + i + 5) % 10 - 5))
            pygame.draw.arc(pantalla, color_agua, (x, caja.bottom - 10 + offset_y, 30, 15), 3.14, 6.28, 2)

        for y in range(caja.top + 20, caja.bottom, 45):
            pygame.draw.line(pantalla, color_agua, (caja.left, y), (caja.left - 10, y + 15), 2)
            pygame.draw.circle(pantalla, color_agua_claro, (caja.left - 10, y + 15), 3)

        for y in range(caja.top + 20, caja.bottom, 45):
            pygame.draw.line(pantalla, color_agua, (caja.right, y), (caja.right + 10, y + 15), 2)
            pygame.draw.circle(pantalla, color_agua_claro, (caja.right + 10, y + 15), 3)

    def crear_patron_lluvia(self, caja, proyectiles):
        for _ in range(4):
            x = random.randint(caja.left + 10, caja.right - 10)
            y = caja.top - random.randint(20, 120)
            proyectiles.append({"rect": pygame.Rect(x, y, 18, 40), "vx": 0, "vy": random.randint(5, 8), "tipo": "lluvia"})

    def crear_patron_lateral(self, caja, proyectiles):
        lado = random.choice(["izquierda", "derecha"])
        for _ in range(2):
            y = random.randint(caja.top + 10, caja.bottom - 20)
            if lado == "izquierda":
                x = caja.left - random.randint(20, 80)
                vx = random.randint(5, 8)
            else:
                x = caja.right + random.randint(20, 80)
                vx = -random.randint(5, 8)
            proyectiles.append({"rect": pygame.Rect(x, y, 34, 20), "vx": vx, "vy": 0, "tipo": "lateral"})

    def crear_patron_diagonal(self, caja, proyectiles):
        for _ in range(3):
            x = random.randint(caja.left + 20, caja.right - 20)
            y = caja.top - random.randint(30, 90)
            vx = random.choice([-3, -2, 2, 3])
            vy = random.randint(4, 6)
            proyectiles.append({"rect": pygame.Rect(x, y, 24, 24), "vx": vx, "vy": vy, "tipo": "diagonal"})

    def pantalla_fin(self, pantalla, fuente_grande, fuente, gano, fondo_img):
        color_titulo = self.COLOR_VERDE if gano else self.COLOR_ROJO
        texto_titulo = "¡HAS GANADO!" if gano else "HAS PERDIDO"
        subtexto = "Sobreviviste a Poseidón..." if gano else "El mar te ha engullido."

        for alpha in range(0, 256, 8):
            pantalla.blit(fondo_img, (0, 0))
            capa = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            capa.fill((0, 0, 20, 210))
            pantalla.blit(capa, (0, 0))

            panel_w, panel_h = 500, 160
            panel_x = self.ancho // 2 - panel_w // 2
            panel_y = self.alto // 2 - panel_h // 2
            panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel.fill((5, 15, 40, min(alpha, 200)))
            pantalla.blit(panel, (panel_x, panel_y))
            pygame.draw.rect(pantalla, color_titulo, (panel_x, panel_y, panel_w, panel_h), 2, border_radius=10)

            surf_titulo = fuente_grande.render(texto_titulo, True, color_titulo)
            surf_titulo.set_alpha(alpha)
            rect_t = surf_titulo.get_rect(center=(self.ancho // 2, self.alto // 2 - 20))
            pantalla.blit(surf_titulo, rect_t)

            surf_sub = fuente.render(subtexto, True, (180, 220, 255))
            surf_sub.set_alpha(alpha)
            rect_s = surf_sub.get_rect(center=(self.ancho // 2, self.alto // 2 + 35))
            pantalla.blit(surf_sub, rect_s)

            pygame.display.flip()
            pygame.time.delay(15)

        pygame.time.delay(1800)

    def jugar(self):
        pygame.init()
        pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("MiniJuego 6 - Combate contra POSEIDÓN")
        reloj = pygame.time.Clock()

        fuente = pygame.font.SysFont("Times New Roman", 26)
        fuente_pequena = pygame.font.SysFont("Times New Roman", 20)
        fuente_grande = pygame.font.SysFont("Times New Roman", 46)
        fuente_label = pygame.font.SysFont("Times New Roman", 16)

        try:
            frames_enemigo = self.cargar_gif("poseidon.gif", escala=(180, 180))  # reducido para dar más espacio de la resolucionn
            if not frames_enemigo:
                raise ValueError("El GIF del enemigo no tiene frames")

            frames_jugador = self.cargar_gif("odiseo.gif", escala=(90, 90))
            if not frames_jugador:
                raise ValueError("El GIF del jugador no tiene frames")

            fondo_img = pygame.image.load("oceano.jpg").convert()
            fondo_img = pygame.transform.scale(fondo_img, (self.ancho, self.alto))

            img_lluvia = pygame.image.load("agua.png").convert_alpha()
            img_lluvia = pygame.transform.scale(img_lluvia, (18, 40))

            img_diagonal = pygame.image.load("tridente.png").convert_alpha()
            img_diagonal = pygame.transform.scale(img_diagonal, (24, 24))

            img_lateral = pygame.image.load("agua.png").convert_alpha()
            img_lateral = pygame.transform.scale(img_lateral, (34, 20))

        except Exception as e:
            print("No se pudo cargar un archivo:", e)
            pygame.quit()
            return False

        frame_actual = 0
        contador_animacion = 0
        frame_jugador_actual = 0
        contador_animacion_jugador = 0

        caja = pygame.Rect(220, 270, 460, 200)  # bajada un poco para dar espacio arriba

        hitbox_ancho, hitbox_alto = 90, 70
        jugador = pygame.Rect(
            caja.centerx - hitbox_ancho // 2,
            caja.centery - hitbox_alto // 2,
            hitbox_ancho, hitbox_alto
        )

        sprite_offset_x = 0
        sprite_offset_y = -20
        velocidad_jugador = 5
        proyectiles = []
        invulnerable = 0
        frame_patron = 0
        tiempo_inicio = pygame.time.get_ticks()
        tick_global = 0
        mirando_derecha = True
        corriendo = True
        gano = False

        while corriendo:
            reloj.tick(self.fps)
            tick_global += 1

            pantalla.blit(fondo_img, (0, 0))
            capa_oscura = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            capa_oscura.fill((0, 0, 0, 70))
            pantalla.blit(capa_oscura, (0, 0))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            tiempo_actual = pygame.time.get_ticks()
            segundos = (tiempo_actual - tiempo_inicio) // 1000
            tiempo_restante = max(0, self.tiempo_supervivencia - segundos)

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and jugador.left > caja.left + 2:
                jugador.x -= velocidad_jugador
                mirando_derecha = True
            if teclas[pygame.K_RIGHT] and jugador.right < caja.right - 2:
                jugador.x += velocidad_jugador
                mirando_derecha = False
            if teclas[pygame.K_UP] and jugador.top > caja.top + 2:
                jugador.y -= velocidad_jugador
            if teclas[pygame.K_DOWN] and jugador.bottom < caja.bottom - 2:
                jugador.y += velocidad_jugador

            frame_patron += 1
            if frame_patron % 28 == 0:
                self.crear_patron_lluvia(caja, proyectiles)
            if frame_patron % 85 == 0:
                self.crear_patron_lateral(caja, proyectiles)
            if frame_patron % 120 == 0:
                self.crear_patron_diagonal(caja, proyectiles)

            for p in proyectiles:
                p["rect"].x += p["vx"]
                p["rect"].y += p["vy"]

            proyectiles = [
                p for p in proyectiles
                if p["rect"].right > caja.left - 120
                and p["rect"].left < caja.right + 120
                and p["rect"].bottom > caja.top - 120
                and p["rect"].top < caja.bottom + 120
            ]

            if invulnerable > 0:
                invulnerable -= 1

            for p in proyectiles[:]:
                if jugador.colliderect(p["rect"]) and invulnerable == 0:
                    self.vida_jugador -= 1
                    invulnerable = 45
                    proyectiles.remove(p)

            contador_animacion += 1
            if contador_animacion >= 24:
                contador_animacion = 0
                frame_actual = (frame_actual + 1) % len(frames_enemigo)

            contador_animacion_jugador += 1
            if contador_animacion_jugador >= 8:
                contador_animacion_jugador = 0
                frame_jugador_actual = (frame_jugador_actual + 1) % len(frames_jugador)

            # ⋆˚☆˖°⋆｡° ✮˖ ࣪ ⊹⋆.˚ DIBUJO ⋆˚☆˖°⋆｡° ✮˖ ࣪ ⊹⋆.˚

            # Enemigo posicion centrada ⋆✴︎˚｡⋆
            frame_enemigo = frames_enemigo[frame_actual]
            rect_enemigo = frame_enemigo.get_rect(center=(self.ancho // 2, 85))  # era 95
            pantalla.blit(frame_enemigo, rect_enemigo)

            # Nombre centrado justo debajo del sprite  ⋆✴︎˚｡⋆
            self.dibujar_texto_centrado(
                pantalla, fuente_label, "— POSEIDÓN —",
                rect_enemigo.bottom + 35,
                self.COLOR_CIAN
            )

            # Frase pulsante con espacio suficiente debajo del nombre  ⋆✴︎˚｡⋆
            pulso = int(160 + 70 * abs((tick_global % 60) / 30 - 1))
            color_frase = (pulso // 3, pulso // 2, pulso)
            texto_frase = "RUTHLESSNESS IS MERCY UPON OURSELVES"
            self.dibujar_texto_centrado(
                pantalla, fuente_pequena, texto_frase,
                rect_enemigo.bottom + 60,  # debajo del nombreee
                color_frase
            )

            self.dibujar_borde_agua(pantalla, caja, tick_global)

            hud_x, hud_y = 30, 30
            self.dibujar_panel_hud(pantalla, hud_x - 8, hud_y - 8, 200, 58)
            self.dibujar_texto_con_sombra(pantalla, fuente_label, "VIDA", hud_x, hud_y, self.COLOR_CIAN)

            pct_vida = self.vida_jugador / self.vida_max
            if pct_vida > 0.5:
                color_vida = (60, 200, 80)
            elif pct_vida > 0.25:
                color_vida = (220, 180, 40)
            else:
                color_vida = (220, 50, 50)

            self.dibujar_barra(pantalla, hud_x, hud_y + 20, 180, 18,
                            self.vida_jugador, self.vida_max, color_vida)
            self.dibujar_texto_con_sombra(
                pantalla, fuente_label,
                f"{self.vida_jugador} / {self.vida_max}",
                hud_x + 60, hud_y + 41, (200, 230, 255)
            )

            hud_t_x = self.ancho - 218
            self.dibujar_panel_hud(pantalla, hud_t_x - 8, hud_y - 8, 200, 58)
            self.dibujar_texto_con_sombra(pantalla, fuente_label, "TIEMPO", hud_t_x, hud_y, self.COLOR_CIAN)

            color_tiempo = (80, 180, 255) if tiempo_restante > 5 else (220, 80, 50)
            self.dibujar_barra(pantalla, hud_t_x, hud_y + 20, 180, 18,
                            tiempo_restante, self.tiempo_supervivencia, color_tiempo,
                            color_vacio=(10, 20, 60))
            self.dibujar_texto_con_sombra(
                pantalla, fuente_label, f"{tiempo_restante}s",
                hud_t_x + 76, hud_y + 41, (200, 230, 255)
            )

            for p in proyectiles:
                if p["tipo"] == "lluvia":
                    pantalla.blit(img_lluvia, (p["rect"].x, p["rect"].y))
                elif p["tipo"] == "diagonal":
                    pantalla.blit(img_diagonal, (p["rect"].x, p["rect"].y))
                elif p["tipo"] == "lateral":
                    pantalla.blit(img_lateral, (p["rect"].x, p["rect"].y))

            if invulnerable % 10 < 5:
                frame_jugador = frames_jugador[frame_jugador_actual]
                if not mirando_derecha:
                    frame_jugador = pygame.transform.flip(frame_jugador, True, False)
                x_dibujo = jugador.centerx - frame_jugador.get_width() // 2 + sprite_offset_x
                y_dibujo = jugador.centery - frame_jugador.get_height() // 2 + sprite_offset_y
                pantalla.blit(frame_jugador, (x_dibujo, y_dibujo))

            if self.vida_jugador <= 0:
                pygame.display.flip()
                self.pantalla_fin(pantalla, fuente_grande, fuente, False, fondo_img)
                corriendo = False
                gano = False

            elif tiempo_restante <= 0:
                pygame.display.flip()
                self.pantalla_fin(pantalla, fuente_grande, fuente, True, fondo_img)
                corriendo = False
                gano = True

            pygame.display.flip()

        pygame.quit()
        return gano


if __name__ == "__main__":
    juego = MiniJuego1()
    resultado = juego.jugar()
    print("Ganó el jugador:", resultado)