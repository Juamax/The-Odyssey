"""
entities/soldier.py — Soldado aliado (Diomedes / Euríloco).
Mismo GIF que Odiseo con tinte de color. IA simple: persigue al
Cíclope y lanza lanzas. Puede morir si el Cíclope lo golpea.
"""

import random
import pygame
from odiseo_vs_ciclope.config import BLUE
from odiseo_vs_ciclope.entities.base import GifEntity
from odiseo_vs_ciclope.projectiles.lance import Lance


class Soldier(GifEntity):
    SPD      = 1.6
    LANCE_CD = 140   # frames entre lanzas

    def __init__(self, frames, x):
        super().__init__(frames, x=x, hp_max=60)
        self.facing   = 1
        self.lance_cd = random.randint(0, self.LANCE_CD)
        self.lances   = []
        self.dying      = False
        self.death_timer = 0

    # ── IA ────────────────────────────────────────────────────

    def update(self, cyclops_x, cyclops_alive):
        if not self.alive: return

        # Animación de muerte progresiva antes de desaparecer
        if self.dying:
            self.death_timer += 1
            self._animate(False)
            if self.death_timer > 70: self.alive = False
            return

        if self.invincible > 0: self.invincible -= 1

        # Mantener ~120 px de distancia con el Cíclope
        if cyclops_alive:
            dx = cyclops_x - self.x
            if   abs(dx) > 120: self.vx, self.facing = self.SPD * (1 if dx>0 else -1), (1 if dx>0 else -1)
            elif abs(dx) < 60:  self.vx = -self.SPD * 0.5 * (1 if dx>0 else -1)
            else:               self.vx = 0
        else:
            self.vx = 0   # se detiene si el Cíclope ya cayó

        self._physics()
        self._animate(abs(self.vx) > 0.1)

        # Disparar lanza hacia el Cíclope
        self.lance_cd -= 1
        if self.lance_cd <= 0 and cyclops_alive:
            ox = self.x + (self.w + 4 if self.facing > 0 else -14)
            self.lances.append(Lance(ox, self.y + self.h * 0.35, self.facing))
            self.lance_cd = self.LANCE_CD

        self.lances = [l for l in self.lances if l.alive]
        for l in self.lances: l.update()

    def start_dying(self):
        self.dying = True
        self.vx    = 0

    def lance_rects(self):
        """Solo devuelve rects de lanzas si el soldado está activo."""
        if self.dying or not self.alive: return []
        return [l.rect() for l in self.lances if l.alive]

    # ── Draw ─────────────────────────────────────────────────

    def draw(self, surf):
        if not self.alive: return
        alpha = max(0, 255 - self.death_timer * 4) if self.dying else 255
        self.draw_sprite(surf, alpha)

        # Barra de HP sobre el soldado
        if not self.dying:
            bx, by = int(self.x), int(self.y) - 9
            pygame.draw.rect(surf, (60, 20, 20), (bx, by, self.w, 5), border_radius=2)
            fill = int(self.w * self.hp / self.hp_max)
            if fill > 0:
                pygame.draw.rect(surf, BLUE, (bx, by, fill, 5), border_radius=2)

        for l in self.lances: l.draw(surf)
