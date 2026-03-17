"""
utils/assets.py — Carga de imágenes y utilidades de sprites.
"""

import pygame


def load_gif_frames(path, scale=None):
    """
    Carga todos los frames de un GIF animado.
    Intenta usar Pillow primero; si no está instalado, carga como imagen estática.
    Retorna lista de surfaces RGBA escaladas.
    """
    frames = []
    try:
        try:
            from PIL import Image as PILImage
            gif = PILImage.open(path)
            for i in range(getattr(gif, 'n_frames', 1)):
                gif.seek(i)
                data = gif.convert("RGBA").tobytes()
                surf = pygame.image.fromstring(data, gif.size, "RGBA")
                if scale:
                    surf = pygame.transform.scale(surf, scale)
                frames.append(surf.convert_alpha())
        except ImportError:
            # Sin Pillow: carga solo el primer frame
            img = pygame.image.load(path)
            if scale:
                img = pygame.transform.scale(img, scale)
            frames.append(img.convert_alpha())
    except Exception as e:
        print(f"[AVISO] No se pudo cargar {path}: {e}")
        # Fallback: cuadrado de color semitransparente
        s = pygame.Surface(scale or (40, 60), pygame.SRCALPHA)
        s.fill((200, 100, 50, 200))
        frames.append(s)
    return frames


def tint_frames(frames, color_rgb, strength=100):
    """
    Devuelve copias de los frames con un tinte de color superpuesto.
    strength: 0 = sin tinte, 255 = tinte total.
    """
    tinted = []
    for frame in frames:
        f = frame.copy()
        overlay = pygame.Surface(f.get_size(), pygame.SRCALPHA)
        overlay.fill((*color_rgb, strength))
        f.blit(overlay, (0, 0))
        tinted.append(f)
    return tinted
