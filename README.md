# ⚓ LA ODISEA

> *"El viaje más largo de la historia, ahora en tus manos."*

Videojuego narrativo basado en **La Odisea de Homero**, desarrollado en Python con Pygame.
Combina una novela visual con estética pergamino/dorado antiguo y minijuegos de acción en los momentos clave de la historia.

---

## 🎮 Descripción

El jugador acompaña a **Odiseo** desde la caída de Troya hasta su regreso a Ítaca, viviendo la historia a través de diálogos con efecto typewriter, banners de capítulo, sprites animados y decisiones que afectan la narrativa. En los momentos de mayor tensión, la novela visual da paso a minijuegos de acción.

---

## 📁 Estructura del Proyecto

```
/
├── main.py                        ← Punto de entrada principal
├── historia1.py                   ← Motor de novela visual + guión completo
│
├── odiseo_vs_ciclope/             ← Minijuego Cap. II — Odiseo vs el Cíclope
│   ├── main.py
│   ├── config.py
│   ├── entities.py
│   ├── ui.py
│   └── utils.py
│
├── Minijuego_poseidon/                 ← Minijuego Cap. III — Tormenta de Poseidón
│   └── mnposeidon2.py
│
├── minijuegos/                    ← Minijuegos generales
│   ├── mncirce.py                 ← Cap. IV — La Isla de Circe
│   └── minijuego1.py              ← Cap. V — El Inframundo
│
├── Minijuego_Zeus/                ← Minijuego Cap. XI — Atenea vs Zeus
│   └── mnzeus.py
│
├── batalla_final/                 ← Minijuego Cap. XIII — Los Pretendientes
│   ├── minijuego5.py
│   ├── personaje.py
│   ├── sistemaOleada2.py
│   ├── entidad2.py
│   └── animacion/fondo/
│
├── Odysseus/                      
│   ├── personaje.py
│   ├── sistemaOleada.py
│   └── entidad.py
│
└── sprites/                       ← Sprites de personajes/pista de audio
```

---

## 📖 Capítulos e Historia

| Cap. | Título | Tipo |
|------|--------|------|
| I | La Caída de Troya | Novela visual + elección |
| II | La Isla del Cíclope | Novela visual + **minijuego** |
| II.I | La Isla Flotante de Eolia | Novela visual |
| III | La Maldición de Poseidón | Novela visual + **minijuego** |
| IV | La Isla de Eea — Circe | Novela visual + **minijuego** |
| V | El Inframundo | Novela visual + **minijuego** |
| VI | Las Sirenas | Novela visual |
| VII | Scylla | Novela visual + elección |
| VIII | El Ganado de Helios | Novela visual |
| IX | Zeus Hace Elegir | Novela visual + elección |
| X | Escapa de Calipso | Novela visual |
| XI | Atenea vs Zeus | Novela visual + **minijuego** |
| XII | Poseidón Pelea | Novela visual |
| XIII | Regreso a Ítaca | Novela visual + **minijuego** |
| XIV | Finalmente con Penélope | Novela visual |

---

## 🕹️ Controles

### Novela Visual
| Tecla | Acción |
|-------|--------|
| `ESPACIO` / `ENTER` | Avanzar diálogo / saltar typewriter |
| `Clic` | Avanzar diálogo |
| `↑ ↓` | Navegar opciones de elección |

### Minijuego — Cíclope
| Tecla | Acción |
|-------|--------|
| `← →` | Mover a Odiseo |
| `ESPACIO` | Saltar |
| `Z` | Lanzar botella de vino |
| `X` | Espadazo al ojo |
| `ESC` | Salir |

### Minijuego — Inframundo / Pretendientes (Beat'em Up)
| Tecla | Acción |
|-------|--------|
| `← → ↑ ↓` | Mover |
| `J` | Ataque rápido |
| `K` | Ataque fuerte |
| `L` | Esquivar |

### Minijuegos — Poseidón / Circe / Zeus (Supervivencia)
| Tecla | Acción |
|-------|--------|
| `← → ↑ ↓` | Mover |

---

## ⚙️ Instalación

### Requisitos
- Python 3.8 o superior
- Pygame
- Pillow

### Instalar dependencias
```bash
pip install pygame pillow
```

### Ejecutar el juego
```bash
python main.py
```

