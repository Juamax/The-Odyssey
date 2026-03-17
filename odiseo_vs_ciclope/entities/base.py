"""
entities/base.py — Clase base GifEntity.
Odiseo y los Soldados heredan de aquí: física, animación,
orientación por flip horizontal y sistema de daño con invencibilidad.
"""

import pygame
from config import GRAVITY, FLOOR_Y, W


class GifEntity:
    """Entidad animada con GIF: física, animación, daño e invencibilidad."""

    def __init__(self, frames, x, hp_max):
        self.frames    = frames
        self.fi        = 0       # índice del frame actual
        self.ftimer    = 0       # contador para avanzar frame
        self.h         = frames[0].get_height()
        self.w         = frames[0].get_width()
        self.x         = float(x)
        self.y         = float(FLOOR_Y - self.h)  # pies sobre FLOOR_Y
        self.vx = self.vy = 0.0
        self.facing    = 1       #  1=derecha  -1=izquierda
        self.on_ground = False
        self.hp        = hp_max
        self.hp_max    = hp_max
        self.invincible = 0
        self.alive     = True

    def _physics(self):
        """Aplica gravedad, mueve la entidad y detecta colisión con el suelo."""
        self.vy += GRAVITY
        self.x  += self.vx
        self.y  += self.vy
        self.on_ground = False
        if self.y + self.h >= FLOOR_Y:
            self.y, self.vy, self.on_ground = float(FLOOR_Y - self.h), 0, True
        self.x = max(0.0, min(self.x, float(W - self.w)))

    def _animate(self, moving, anim_speed=1.0):
        """
        Avanza el frame del GIF.
        anim_speed > 1 → más lenta (más ticks por frame).
        """
        spd = int((10 if moving else 24) * anim_speed)
        self.ftimer += 1
        if self.ftimer >= spd:
            self.ftimer = 0
            self.fi = (self.fi + 1) % len(self.frames)

    def get_rect(self):
        return pygame.Rect(int(self.x) + 4, int(self.y), self.w - 8, self.h)

    def take_damage(self, dmg):
        """Aplica daño si no está en período de invencibilidad. Retorna True si fue golpeado."""
        if self.invincible > 0 or not self.alive:
            return False
        self.hp -= dmg
        self.invincible = 54
        if self.hp <= 0:
            self.hp    = 0
            self.alive = False
        return True

    def draw_sprite(self, surf, alpha=255):
        """
        Dibuja el frame actual con la orientación correcta.
        El GIF mira a la izquierda por defecto:
          facing =  1 (derecha) → flip horizontal
          facing = -1 (izquierda) → sin flip
        Parpadea durante el período de invencibilidad.
        """
        if self.invincible > 0 and (self.invincible // 5) % 2:
            return
        frame = self.frames[self.fi]
        if alpha < 255:
            frame = frame.copy()
            frame.set_alpha(alpha)
        surf.blit(pygame.transform.flip(frame, self.facing > 0, False),
                  (int(self.x), int(self.y)))
