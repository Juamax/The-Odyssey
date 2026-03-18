"""
projectiles/bottle.py — Botella de vino lanzada por Odiseo.
Al impactar al Cíclope activa su estado de tambaleo (stun).
"""

import pygame
from odiseo_vs_ciclope.config import GRAVITY, FLOOR_Y, W, WINE, WHITE


class Bottle:
    def __init__(self, x, y, direction):
        self.x, self.y = float(x), float(y)
        self.vx    = 6.0 * direction
        self.vy    = -3.2
        self.alive = True

    def update(self):
        self.vy += GRAVITY * 0.8
        self.x  += self.vx
        self.y  += self.vy
        # Destruir si sale de pantalla o toca el suelo
        if self.y > FLOOR_Y + 30 or not (-20 < self.x < W + 20):
            self.alive = False

    def rect(self):
        return pygame.Rect(int(self.x) - 5, int(self.y) - 8, 10, 16)

    def draw(self, surf):
        cx, cy = int(self.x), int(self.y)
        pygame.draw.ellipse(surf, WINE,  (cx - 5, cy - 8,  10, 14))
        pygame.draw.rect   (surf, WINE,  (cx - 3, cy - 14,  6,  8))
        pygame.draw.rect   (surf, WHITE, (cx - 2, cy - 16,  4,  3))
