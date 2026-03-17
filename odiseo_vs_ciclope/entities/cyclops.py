"""
entities/cyclops.py — El Cíclope, villano principal.
Cambios respecto a la versión original:
  - Flip horizontal según dirección de movimiento.
  - Animación 1.6x más lenta (anim_speed=1.6).
  - HP aumentado 30%: 200 → 260.
  - Efecto de tambaleo (oscilación lateral) cuando está borracho por el vino.
"""

import pygame
import random
import math
from config import W, FLOOR_Y, RED


class Cyclops:
    SPEED        = 1.1
    DRUNK_FRAMES = 215
    ANIM_SPEED   = 1.6   # factor de ralentización de la animación

    def __init__(self, frames):
        self.frames     = frames
        self.fi         = 0
        self.ftimer     = 0
        self.h          = frames[0].get_height()
        self.w          = frames[0].get_width()
        self.x          = float(W - self.w - 60)
        self.y          = float(FLOOR_Y - self.h)
        self.hp         = 260          # +30% respecto a 200
        self.max_hp     = 260
        self.drunk      = 0
        self.invincible = 0
        self.alive      = True
        self.death_timer = 0
        self.rage       = False
        self.facing     = -1           # -1=izquierda (default), 1=derecha
        self.wobble     = 0.0          # fase del tambaleo lateral al estar borracho
        self.particles  = []

    # ── Impacto y aturdimiento ────────────────────────────────

    def take_hit(self, dmg):
        """Aplica daño al ojo. Genera partículas de impacto. Retorna True si fue golpeado."""
        if self.invincible > 0 or not self.alive:
            return False
        self.hp        -= dmg
        self.invincible = 18
        cx = self.x + self.w // 2
        for _ in range(14):
            self.particles.append({
                "x": cx, "y": self.y + 40,
                "vx": random.uniform(-4, 4), "vy": random.uniform(-5, -1),
                "life": random.randint(25, 45),
                "color": random.choice([(255,80,20),(255,200,50),(220,50,50)]),
            })
        if self.hp <= 0:
            self.hp, self.alive = 0, False
        return True

    def stun(self):
        """Activa el tambaleo por vino."""
        self.drunk  = self.DRUNK_FRAMES
        self.wobble = 0.0

    # ── Update ────────────────────────────────────────────────

    def update(self, player_x):
        if self.invincible > 0: self.invincible -= 1
        if self.drunk      > 0: self.drunk      -= 1
        self.rage = self.hp < self.max_hp * 0.3

        # Si ya murió: solo avanza death_timer y partículas
        if not self.alive:
            self.death_timer += 1
            self._update_particles()
            return

        # Velocidad afectada por borrachera y rabia
        mult = 0.25 if self.drunk > 0 else (1.5 if self.rage else 1.0)
        dx   = player_x - self.x

        # Actualizar posición y orientación (flip según dirección)
        self.x      += self.SPEED * mult * (1 if dx > 0 else -1)
        self.x       = max(0.0, min(self.x, float(W - self.w)))
        self.facing  = -1 if dx > 0 else 1   # sigue al jugador con el cuerpo

        # Tambaleo lateral cuando está borracho: desplazamiento X sinusoidal
        if self.drunk > 0:
            self.wobble += 0.18
            # El offset se aplica solo al dibujo (ver draw)

        # Animación más lenta con ANIM_SPEED; aún más lenta si borracho
        speed_factor = self.ANIM_SPEED * (1.5 if self.drunk > 0 else 1.0)
        spd = int(12 * speed_factor)
        self.ftimer += 1
        if self.ftimer >= spd:
            self.ftimer = 0
            self.fi = (self.fi + 1) % len(self.frames)

        self._update_particles()

    def _update_particles(self):
        for p in self.particles[:]:
            p["x"] += p["vx"]; p["y"] += p["vy"]
            p["vy"] += 0.2;    p["life"] -= 1
            if p["life"] <= 0: self.particles.remove(p)

    # ── Rectángulos de colisión ───────────────────────────────

    def eye_rect(self):
        return pygame.Rect(int(self.x) + self.w//2 - 28, int(self.y) + 20, 56, 50)

    def body_rect(self):
        return pygame.Rect(int(self.x) + 20, int(self.y) + 30, self.w - 40, self.h - 30)

    # ── Draw ─────────────────────────────────────────────────

    def draw(self, surf):
        # Partículas de impacto (fuego/chispas)
        for p in self.particles:
            pygame.draw.circle(surf, p["color"],
                               (int(p["x"]), int(p["y"])), max(1, p["life"] // 8))

        # Animación de desvanecimiento al morir
        if not self.alive:
            if self.death_timer < 90:
                f = self.frames[self.fi].copy()
                f.set_alpha(max(0, 255 - self.death_timer * 3))
                surf.blit(f, (int(self.x), int(self.y)))
            return

        # Parpadeo de invencibilidad
        if self.invincible > 0 and (self.invincible // 4) % 2:
            return

        frame = self.frames[self.fi]

        # Overlay azulado cuando está borracho
        if self.drunk > 0:
            frame = frame.copy()
            ov = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            ov.fill((50, 50, 200, 55))
            frame.blit(ov, (0, 0))

        # Flip según dirección de movimiento
        frame = pygame.transform.flip(frame, self.facing > 0, False)

        # Tambaleo: offset sinusoidal en X cuando está borracho
        wobble_offset = int(math.sin(self.wobble) * 10) if self.drunk > 0 else 0

        surf.blit(frame, (int(self.x) + wobble_offset, int(self.y)))

        # Texto de aturdimiento
        if self.drunk > 0:
            fnt = pygame.font.SysFont("Arial", 15, bold=True)
            cx  = int(self.x) + self.w // 2 + wobble_offset
            t   = fnt.render("★ ATURDIDO ★", True, (200, 120, 255))
            surf.blit(t, (cx - t.get_width() // 2, int(self.y) - 22))

        # Barra de vida
        bw = 120
        bx = int(self.x) + self.w // 2 - bw // 2
        by = int(self.y) - 16
        pygame.draw.rect(surf, (60, 30, 30), (bx, by, bw, 12), border_radius=4)
        fill = int(bw * self.hp / self.max_hp)
        if fill > 0:
            pygame.draw.rect(surf, RED, (bx, by, fill, 12), border_radius=4)
