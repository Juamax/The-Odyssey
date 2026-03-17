"""
entities/player.py — Odiseo, el jugador.
Controles: ← → moverse, ESPACIO saltar, Z lanzar vino, X espadazo.
Nuevo: efecto de victoria con salto + partículas doradas.
"""

import pygame
import random
from config import GRAVITY, JUMP, SPEED, FLOOR_Y, GOLD, WHITE
from .base import GifEntity
from projectiles.bottle import Bottle


class Player(GifEntity):
    WINE_CD  = 34   # cooldown lanzar botella (frames)
    SWORD_CD = 26   # cooldown espadazo (frames)

    def __init__(self, frames):
        super().__init__(frames, x=80, hp_max=100)
        self.lives        = 3
        self.score        = 0
        self.bottles      = []
        self.wine_cd      = 0
        self.sword_cd     = 0
        self.sword_active = 0

        # Efecto de victoria
        self.victory        = False
        self.victory_jump   = False   # ¿ya inició el salto?
        self.victory_particles = []

    # ── Input y acciones ──────────────────────────────────────

    def handle_input(self, keys):
        self.vx = 0
        if keys[pygame.K_LEFT]:  self.vx, self.facing = -SPEED, -1
        if keys[pygame.K_RIGHT]: self.vx, self.facing =  SPEED,  1
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = JUMP

    def throw_wine(self):
        if self.wine_cd > 0: return
        ox = self.x + (self.w + 4 if self.facing > 0 else -14)
        self.bottles.append(Bottle(ox, self.y + self.h * 0.35, self.facing))
        self.wine_cd = self.WINE_CD

    def sword_attack(self):
        if self.sword_cd > 0: return
        self.sword_active = 17
        self.sword_cd     = self.SWORD_CD

    def sword_rect(self):
        if self.sword_active <= 0:
            return pygame.Rect(0, 0, 0, 0)
        if self.facing > 0:
            return pygame.Rect(int(self.x) + self.w, int(self.y) + 5, 55, 40)
        return     pygame.Rect(int(self.x) - 55,     int(self.y) + 5, 55, 40)

    # ── Victoria ──────────────────────────────────────────────

    def trigger_victory(self):
        """Inicia el salto de celebración y genera partículas doradas."""
        self.victory = True
        self.vy      = JUMP * 1.1   # salto más alto que el normal
        # Generar explosión de partículas doradas desde el centro del sprite
        cx = self.x + self.w // 2
        cy = self.y + self.h // 2
        for _ in range(40):
            self.victory_particles.append({
                "x": cx, "y": cy,
                "vx": random.uniform(-5, 5),
                "vy": random.uniform(-7, -1),
                "life": random.randint(30, 60),
                "r":    random.randint(3, 7),
            })

    def _update_victory_particles(self):
        for p in self.victory_particles[:]:
            p["x"]  += p["vx"]
            p["y"]  += p["vy"]
            p["vy"] += GRAVITY * 0.5   # caída suave
            p["life"] -= 1
            if p["life"] <= 0:
                self.victory_particles.remove(p)

    # ── Update / Draw ─────────────────────────────────────────

    def update(self):
        # Decrementar cooldowns
        if self.wine_cd      > 0: self.wine_cd      -= 1
        if self.sword_cd     > 0: self.sword_cd     -= 1
        if self.sword_active > 0: self.sword_active -= 1
        if self.invincible   > 0: self.invincible   -= 1

        self._physics()
        self._animate(abs(self.vx) > 0.1)

        # Botellas en vuelo
        self.bottles = [b for b in self.bottles if b.alive]
        for b in self.bottles: b.update()

        if self.victory:
            self._update_victory_particles()

    def draw(self, surf):
        self.draw_sprite(surf)

        # Arco visual del espadazo
        if self.sword_active > 0:
            sr = self.sword_rect()
            s  = pygame.Surface((sr.w, sr.h), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (*GOLD, int(180 * self.sword_active / 17)),
                                (0, 0, sr.w, sr.h))
            surf.blit(s, (sr.x, sr.y))

        # Partículas de victoria
        for p in self.victory_particles:
            alpha = int(255 * p["life"] / 60)
            pygame.draw.circle(surf, (*GOLD, alpha),
                               (int(p["x"]), int(p["y"])), p["r"])

        for b in self.bottles: b.draw(surf)
