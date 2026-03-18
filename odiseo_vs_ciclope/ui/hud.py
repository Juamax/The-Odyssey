"""
ui/hud.py — Interfaz gráfica superpuesta al juego.
Incluye: HUD de vida/score, pantallas de overlay y secuencia de victoria.
La secuencia de victoria ya NO muestra texto "¡VICTORIA!" — salta
directo a las imágenes con fade-in.
"""

import pygame, sys
from odiseo_vs_ciclope.config import W, H, FPS, BLACK, WHITE, RED, GREEN, GOLD, GRAY, BLUE


# ── HUD en juego ──────────────────────────────────────────────

def draw_hud(surf, player, soldiers, font_m, font_s):
    """Dibuja la barra de vida, vidas, score y HP de soldados."""
    panel = pygame.Surface((W, 48), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 140))
    surf.blit(panel, (0, 0))

    # Barra de vida de Odiseo
    pygame.draw.rect(surf, (80, 20, 20), (10, 10, 150, 14), border_radius=4)
    fill = int(150 * player.hp / 100)
    if fill > 0:
        pygame.draw.rect(surf, GREEN, (10, 10, fill, 14), border_radius=4)
    surf.blit(font_s.render("ODISEO", True, WHITE), (12, 11))

    # Círculos de vidas
    for i in range(player.lives):
        pygame.draw.circle(surf, RED, (172 + i * 20, 17), 7)

    # Score centrado
    sc = f"SCORE {player.score}"
    surf.blit(font_m.render(sc, True, GOLD),
              (W // 2 - font_m.size(sc)[0] // 2, 10))

    # HP de soldados vivos (arriba derecha)
    names = ["Diomedes", "Euríloco"]
    vivos = [s for s in soldiers if s.alive and not s.dying]
    for i, sol in enumerate(vivos[:2]):
        bx, by, bw = W - 105, 10 + i * 20, 90
        pygame.draw.rect(surf, (30, 30, 80), (bx, by, bw, 11), border_radius=3)
        f2 = int(bw * sol.hp / sol.hp_max)
        if f2 > 0:
            pygame.draw.rect(surf, BLUE, (bx, by, f2, 11), border_radius=3)
        surf.blit(font_s.render(names[i], True, WHITE), (bx - 72, by))

    # Controles
    surf.blit(font_s.render(
        "← →: Mover  ESPACIO: Saltar  Z: Vino  X: Espada",
        True, GRAY), (W // 2 - 200, H - 18))


# ── Pantallas de overlay ──────────────────────────────────────

def draw_overlay_screen(surf, bg, lines):
    """Dibuja fondo + capa oscura + líneas de texto centradas."""
    surf.blit(bg, (0, 0))
    ov = pygame.Surface((W, H), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 175))
    surf.blit(ov, (0, 0))
    for text, font, color, y in lines:
        t = font.render(text, True, color)
        surf.blit(t, (W // 2 - t.get_width() // 2, y))
    pygame.display.flip()


# ── Secuencia de victoria ─────────────────────────────────────

def show_victory_sequence(screen, clock, font_big, font_med, img_vence, img_escapa):
    """
    Secuencia post-victoria: dos imágenes con fade-in.
    Sin texto de "¡VICTORIA!" — salta directo a las imágenes.
    Escena 1: img_vence  (Odiseo vence al Cíclope)
    Escena 2: img_escapa (Odiseo escapa de la cueva)
    """
    def scale_fit(img):
        iw, ih = img.get_size()
        sc = min(W / iw, H / ih)
        return pygame.transform.scale(img, (int(iw * sc), int(ih * sc)))

    img1 = scale_fit(img_vence)
    img2 = scale_fit(img_escapa)

    def _show_scene(img, caption):
        """Fade-in de una imagen + caption parpadeante. ENTER para continuar."""
        alpha   = 0
        waiting = True
        while waiting:
            clock.tick(FPS)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:          pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                    waiting = False
            screen.fill(BLACK)
            img_c = img.copy()
            img_c.set_alpha(min(alpha, 255))
            screen.blit(img_c, ((W - img.get_width()) // 2,
                                 (H - img.get_height()) // 2))
            alpha = min(alpha + 4, 255)
            # Caption + indicación solo cuando la imagen ya es visible
            if alpha >= 255:
                bar = pygame.Surface((W, 65), pygame.SRCALPHA)
                bar.fill((0, 0, 0, 165))
                screen.blit(bar, (0, H - 85))
                t1 = font_big.render(caption, True, GOLD)
                screen.blit(t1, (W // 2 - t1.get_width() // 2, H - 80))
                if (pygame.time.get_ticks() // 500) % 2:
                    t2 = font_med.render("[ ENTER ] continuar", True, WHITE)
                    screen.blit(t2, (W // 2 - t2.get_width() // 2, H - 42))
            pygame.display.flip()

    _show_scene(img1, "")
    _show_scene(img2, "¡Odiseo escapa de la cueva!")
