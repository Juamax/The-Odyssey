"""
projectiles/lance.py — Lanza disparada por los soldados aliados.
Viaja horizontalmente y hace daño menor al Cíclope.
"""

import pygame
from config import W, WHITE


class Lance:
    def __init__(self, x, y, direction):
        self.x, self.y = float(x), float(y)
        self.vx    = 5.6 * direction
        self.dir   = direction
        self.alive = True

    def update(self):
        self.x += self.vx
        if not (-20 < self.x < W + 20):
            self.alive = False

    def rect(self):
        return pygame.Rect(int(self.x) - 3, int(self.y) - 3, 20, 6)

    def draw(self, surf):
        lx, ly = int(self.x), int(self.y)
        pygame.draw.line   (surf, (200, 180, 80), (lx, ly), (lx + 18 * self.dir, ly), 2)
        pygame.draw.polygon(surf, WHITE, [
            (lx + 20 * self.dir, ly),
            (lx + 11 * self.dir, ly - 4),
            (lx + 11 * self.dir, ly + 4),
        ])
