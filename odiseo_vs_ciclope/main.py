"""
main.py — Entry point de ODISEO VS EL CÍCLOPE.
Maneja el game loop, estados (menu / playing / gameover / win)
y la comunicación entre todos los módulos.

CONTROLES
  ← →       Mover
  ESPACIO   Saltar
  Z         Lanzar botella de vino
  X         Espadazo (solo daña al ojo del Cíclope)
  ESC       Menú / Salir

Instalación: pip install pygame pillow
"""

import pygame, sys

from config   import W, H, FPS, FLOOR_Y, BLACK, WHITE, RED, GOLD, GRAY
from utils    import load_gif_frames, Amphora
from entities import Player, Cyclops, Soldier
from ui       import draw_hud, draw_overlay_screen, show_victory_sequence


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("ODISEO VS EL CÍCLOPE")
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Arial", 46, bold=True)
    font_med = pygame.font.SysFont("Arial", 26, bold=True)
    font_s   = pygame.font.SysFont("Arial", 15)

    # ── Cargar assets ─────────────────────────────────────────
    odiseo_frames  = load_gif_frames("odiseo.gif",  scale=(75,  90))
    ciclope_frames = load_gif_frames("ciclope.gif", scale=(220, 300))
    soldier_frames = [
        load_gif_frames("soldado.png", scale=(75, 90)),
        load_gif_frames("soldado.png", scale=(75, 90)),
    ]

    def load_img(path, color_fallback):
        try:   return pygame.image.load(path).convert()
        except Exception:
            s = pygame.Surface((W, H)); s.fill(color_fallback); return s

    bg        = load_img("cueva.jpg",                (20, 12, 30))
    img_vence = load_img("odiseo_vence_ciclope.PNG", (50, 20, 10))
    img_escapa= load_img("odiseo_escapa_cueva.PNG",  (10, 30, 60))
    try: bg = pygame.transform.scale(pygame.image.load("cueva.jpg").convert(), (W, H))
    except: pass

    state = "menu"

    # ══════════════════════════════════════════════════════════
    while True:

        # ── MENÚ ─────────────────────────────────────────────
        if state == "menu":
            blink = (pygame.time.get_ticks() // 500) % 2 == 0
            lines = [
                ("ODISEO vs EL CÍCLOPE",         font_big, GOLD,  110),
                ("— La Odisea, Canto IX —",       font_med, WHITE, 175),
                ("Z — Lanzar vino para aturdir",  font_s,   WHITE, 252),
                ("X — Espadazo en el ojo",        font_s,   WHITE, 280),
                ("Recoge ánforas: vida y vino",   font_s,   WHITE, 308),
                ("Diomedes y Euríloco te apoyan", font_s,   WHITE, 336),
            ]
            if blink:
                lines.append(("[ ENTER ] para comenzar", font_med, GOLD, 400))
            draw_overlay_screen(screen, bg, lines)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN: state = "playing"
                    if ev.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
            clock.tick(FPS)
            continue

        # ── INIT partida ──────────────────────────────────────
        player   = Player(odiseo_frames)
        cyclops  = Cyclops(ciclope_frames)
        soldiers = [
            Soldier(soldier_frames[0], x=200),
            Soldier(soldier_frames[1], x=290),
        ]
        amphorae = [
            Amphora(300, FLOOR_Y - 26, "life"),
            Amphora(500, FLOOR_Y - 26, "wine"),
            Amphora(680, FLOOR_Y - 26, "life"),
        ]
        result         = None
        victory_timer  = 0   # frames de espera tras victoria antes de mostrar imágenes

        # ── LOOP de partida ───────────────────────────────────
        while result is None:
            clock.tick(FPS)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE: state = "menu"; break
                    if ev.key == pygame.K_z:      player.throw_wine()
                    if ev.key == pygame.K_x:      player.sword_attack()
            else:
                keys = pygame.key.get_pressed()

                # ── Actualizar entidades ──────────────────────
                if not player.victory:
                    player.handle_input(keys)
                player.update()

                cyclops.update(player.x)
                for sol in soldiers:
                    sol.update(cyclops.x, cyclops.alive)
                for amp in amphorae:
                    amp.update()

                # ── Efecto de victoria (salto + partículas) ───
                if player.victory:
                    victory_timer += 1
                    if victory_timer >= 90:   # espera ~1.5 s y pasa a imágenes
                        result = "win"
                    # loop de física para que el salto se vea
                    continue

                # ── Colisiones: botellas → Cíclope ───────────
                for b in player.bottles[:]:
                    if cyclops.alive and b.rect().colliderect(cyclops.body_rect()):
                        cyclops.stun()
                        b.alive = False
                        player.score += 20

                # ── Colisiones: espada → ojo del Cíclope ─────
                if player.sword_active > 0 and cyclops.alive:
                    if player.sword_rect().colliderect(cyclops.eye_rect()):
                        if cyclops.take_hit(40):
                            player.score += 50
                            if not cyclops.alive:
                                # Dispara el efecto de victoria
                                player.trigger_victory()

                # ── Colisiones: lanzas de soldados → Cíclope ─
                for sol in soldiers:
                    for lr in sol.lance_rects():
                        if cyclops.alive and lr.colliderect(cyclops.body_rect()):
                            cyclops.hp = max(1, cyclops.hp - 4)
                            player.score += 5
                            # Eliminar lanza al impactar
                            for l in sol.lances:
                                if l.alive and l.rect().colliderect(lr):
                                    l.alive = False; break

                # ── Cíclope daña a Odiseo y soldados ─────────
                if cyclops.alive and cyclops.drunk == 0:
                    br = cyclops.body_rect().inflate(-20, -20)
                    if br.colliderect(player.get_rect()):
                        if player.take_damage(9):
                            player.vx = 5 * (-1 if player.x > cyclops.x else 1)
                            player.vy = -3.5
                    for sol in soldiers:
                        if not sol.alive or sol.dying: continue
                        if br.colliderect(sol.get_rect()):
                            if sol.take_damage(8) and sol.hp <= 0:
                                sol.start_dying()

                # ── Recoger ánforas ───────────────────────────
                pr = player.get_rect()
                for amp in amphorae:
                    if amp.alive and amp.rect().colliderect(pr):
                        amp.alive = False
                        if amp.kind == "life": player.hp = min(100, player.hp + 30)
                        else:                  player.wine_cd = 0
                        player.score += 10

                # ── Odiseo pierde vida ────────────────────────
                if not player.alive:
                    player.lives -= 1
                    if player.lives > 0:
                        player.hp, player.alive = 100, True
                        player.x  = 80.0
                        player.y  = float(FLOOR_Y - player.h)
                        player.invincible = 90
                    else:
                        result = "gameover"

                # ── Dibujo del frame ──────────────────────────
                screen.blit(bg, (0, 0))
                for amp in amphorae:
                    if amp.alive: amp.draw(screen)
                cyclops.draw(screen)
                for sol in soldiers: sol.draw(screen)
                player.draw(screen)
                draw_hud(screen, player, soldiers, font_med, font_s)
                pygame.display.flip()
                continue

            if state == "menu": break

        # ── Resultado ─────────────────────────────────────────
        if result == "win":
            show_victory_sequence(screen, clock, font_big, font_med,
                                   img_vence, img_escapa)
            state = "menu"

        elif result == "gameover":
            lines = [
                ("GAME OVER",                   font_big, RED,   150),
                ("Odiseo no logró escapar...",   font_med, WHITE, 230),
                (f"Puntuación: {player.score}",  font_med, GOLD,  275),
                ("[ ENTER ] intentar de nuevo",  font_med, WHITE, 350),
                ("[ ESC ] menú",                 font_s,   GRAY,  390),
            ]
            draw_overlay_screen(screen, bg, lines)
            waiting = True
            while waiting:
                clock.tick(FPS)
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_RETURN: state = "playing"; waiting = False
                        if ev.key == pygame.K_ESCAPE: state = "menu";    waiting = False


if __name__ == "__main__":
    main()
