"""
utils/amphora.py — Power-up coleccionable (ánfora).
Tipos: "life" recupera HP, "wine" resetea cooldown de vino.
"""

import math
import pygame
from odiseo_vs_ciclope.config import FLOOR_Y, GOLD, WINE, WHITE


class Amphora:
    def __init__(self, x, y, kind):
        self.x, self.y = x, y
        self.kind  = kind   # "life" o "wine"
        self.alive = True
        self.bob   = 0.0    # oscilación vertical animada

    def rect(self):
        return pygame.Rect(self.x - 10, self.y - 18, 20, 22)

    def update(self):
        self.bob += 0.05    # avanza la fase del seno para flotar

    def draw(self, surf):
        cy  = self.y + int(math.sin(self.bob) * 4)
        col = GOLD if self.kind == "life" else WINE
        pygame.draw.ellipse(surf, col,   (self.x - 8,  cy - 10, 16, 18))
        pygame.draw.rect   (surf, col,   (self.x - 3,  cy - 17,  6,  9))
        pygame.draw.rect   (surf, WHITE, (self.x - 5,  cy - 18, 10,  3))
        fnt = pygame.font.SysFont("Arial", 11, bold=True)
        t   = fnt.render("+HP" if self.kind == "life" else "+VIN", True, WHITE)
        surf.blit(t, (self.x - t.get_width() // 2, cy - 30))
