import pygame
import sys
import os
import random
import math
# ꧁ ༺ ⚜ ༻ ꧂  VelvetProyect — LA ODISEA: Motor de Novela Visual  ꧁ ༺ ⚜ ༻ ꧂

# ══════════════════════════════════════════════════════════
#  CONFIGURACIÓN GLOBAL
# ══════════════════════════════════════════════════════════
ANCHO, ALTO = 900, 550
FPS = 60

# ── Paleta Pergamino / Dorado Antiguo ────────────────────
C_PERGAMINO      = (245, 228, 180)
C_PERGAMINO_OSC  = (200, 175, 110)
C_ORO            = (212, 170,  55)
C_ORO_CLARO      = (255, 230, 120)
C_ORO_OSC        = (130, 100,  25)
C_TINTA          = ( 28,  18,   6)
C_SOMBRA         = (  0,   0,   0)
C_NOMBRE_BG      = ( 50,  35,   8, 245)
C_PANEL_BG       = ( 22,  14,   3, 220)
C_ELEC_INACTIVO  = ( 40,  28,   8, 210)
C_FONDO_BASE     = ( 10,   6,   2)

# ── Caja de diálogo ──────────────────────────────────────
CAJA_H    = 160
CAJA_Y    = ALTO - CAJA_H - 12
CAJA_X    = 20
CAJA_W    = ANCHO - 40
NOMBRE_H  = 30
NOMBRE_W  = 230

# ── Sprite del personaje ─────────────────────────────────
SPRITE_ALTO  = 260
SPRITE_ANCHO = 200

# ── Typewriter ───────────────────────────────────────────
CHARS_POR_FRAME = 1
DELAY_CHAR_MS   = 28

# ══════════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════════

def cargar_imagen(ruta, escala=None, alpha=False):
    if not ruta or not os.path.exists(ruta):
        return None
    try:
        img = pygame.image.load(ruta)
        img = img.convert_alpha() if alpha else img.convert()
        if escala:
            img = pygame.transform.scale(img, escala)
        return img
    except Exception:
        return None

def cargar_imagen_proporcional(ruta, alto_max, ancho_max):
    if not ruta or not os.path.exists(ruta):
        return None
    try:
        img = pygame.image.load(ruta).convert_alpha()
        w, h = img.get_size()
        escala = min(alto_max / h, ancho_max / w)
        nuevo_w = int(w * escala)
        nuevo_h = int(h * escala)
        return pygame.transform.smoothscale(img, (nuevo_w, nuevo_h))
    except Exception:
        return None

def cargar_musica(ruta):
    if not ruta or not os.path.exists(ruta):
        return False
    try:
        pygame.mixer.music.load(ruta)
        return True
    except Exception:
        return False

# ══════════════════════════════════════════════════════════
#  MOTOR PRINCIPAL
# ══════════════════════════════════════════════════════════

class NovelVisual:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("La Odisea  ⚓  VelvetProyect")
        self.reloj = pygame.time.Clock()

        self.f_texto  = pygame.font.SysFont("Times New Roman", 22)
        self.f_nombre = pygame.font.SysFont("Times New Roman", 19, bold=True)
        self.f_label  = pygame.font.SysFont("Times New Roman", 13)
        self.f_titulo = pygame.font.SysFont("Times New Roman", 36, bold=True)
        self.f_sub    = pygame.font.SysFont("Times New Roman", 18)
        self.f_elec   = pygame.font.SysFont("Times New Roman", 20)
        self.f_cap    = pygame.font.SysFont("Times New Roman", 14)

        self._fondos   = {}
        self._sprites  = {}
        self.fondo_actual  = None
        self.sprite_actual = None
        self.sprite_lado   = "izq"

        self.escena_idx = 0
        self._respuesta_pendiente = None

        self._tw_texto_total  = ""
        self._tw_chars_vis    = 0
        self._tw_ultimo_tick  = 0
        self._tw_completo     = False

        self.opciones_elec = []
        self.opcion_hover  = 0

        self._tex_perg = self._gen_textura_pergamino()
        self.escenas = self._construir_escenas()

    # ══════════════════════════════════════════════════════
    #  TEXTURA PERGAMINO
    # ══════════════════════════════════════════════════════
    def _gen_textura_pergamino(self):
        s = pygame.Surface((CAJA_W, CAJA_H), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        for _ in range(2000):
            x = random.randint(0, CAJA_W - 1)
            y = random.randint(0, CAJA_H - 1)
            v = random.randint(170, 255)
            a = random.randint(3, 12)
            s.set_at((x, y), (v, v, v, a))
        return s

    # ══════════════════════════════════════════════════════
    #  DIBUJO
    # ══════════════════════════════════════════════════════
    def _dibujar_fondo(self):
        if self.fondo_actual:
            self.pantalla.blit(self.fondo_actual, (0, 0))
        else:
            self.pantalla.fill(C_FONDO_BASE)

    def _capa_oscura(self, alpha=85):
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, alpha))
        self.pantalla.blit(s, (0, 0))

    def _dibujar_sprite(self):
        if not self.sprite_actual:
            return
        sp = self.sprite_actual
        sw, sh = sp.get_size()
        sy = CAJA_Y - sh + 10
        if self.sprite_lado == "izq":
            sx = 60
        elif self.sprite_lado == "der":
            sx = ANCHO - sw - 60
        else:
            sx = ANCHO // 2 - sw // 2
        sombra = pygame.Surface((sw, 18), pygame.SRCALPHA)
        for i in range(18):
            alpha_s = int(80 * (1 - i / 18))
            pygame.draw.ellipse(sombra, (0, 0, 0, alpha_s),
                                (sw//8, i//2, sw*3//4, 18 - i//2))
        self.pantalla.blit(sombra, (sx, CAJA_Y - 14))
        self.pantalla.blit(sp, (sx, sy))

    # ══════════════════════════════════════════════════════
    #  TYPEWRITER
    # ══════════════════════════════════════════════════════
    def _tw_iniciar(self, texto):
        self._tw_texto_total = texto
        self._tw_chars_vis   = 0
        self._tw_ultimo_tick = pygame.time.get_ticks()
        self._tw_completo    = False

    def _tw_actualizar(self):
        if self._tw_completo:
            return
        ahora = pygame.time.get_ticks()
        avances = (ahora - self._tw_ultimo_tick) // DELAY_CHAR_MS
        if avances > 0:
            self._tw_chars_vis = min(
                self._tw_chars_vis + avances * CHARS_POR_FRAME,
                len(self._tw_texto_total)
            )
            self._tw_ultimo_tick = ahora
            if self._tw_chars_vis >= len(self._tw_texto_total):
                self._tw_completo = True

    def _tw_saltar(self):
        self._tw_chars_vis = len(self._tw_texto_total)
        self._tw_completo  = True

    # ══════════════════════════════════════════════════════
    #  CAJA DE DIÁLOGO
    # ══════════════════════════════════════════════════════
    def _dibujar_caja(self, nombre, texto_visible):
        x, y, w, h = CAJA_X, CAJA_Y, CAJA_W, CAJA_H

        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill(C_PANEL_BG)
        self.pantalla.blit(panel, (x, y))
        self.pantalla.blit(self._tex_perg, (x, y))

        pygame.draw.rect(self.pantalla, C_ORO, (x, y, w, h), 3, border_radius=4)
        pygame.draw.rect(self.pantalla, C_ORO_OSC, (x+5, y+5, w-10, h-10), 1, border_radius=2)

        for cx, cy in [(x+14, y+14), (x+w-14, y+14),
                       (x+14, y+h-14), (x+w-14, y+h-14)]:
            pts = [(cx, cy-6), (cx+6, cy), (cx, cy+6), (cx-6, cy)]
            pygame.draw.polygon(self.pantalla, C_ORO, pts)
            pygame.draw.polygon(self.pantalla, C_ORO_OSC, pts, 1)

        pygame.draw.line(self.pantalla, C_ORO_OSC, (x+26, y+38), (x+w-26, y+38), 1)

        if nombre:
            np = pygame.Surface((NOMBRE_W, NOMBRE_H), pygame.SRCALPHA)
            np.fill(C_NOMBRE_BG)
            self.pantalla.blit(np, (x, y - NOMBRE_H + 2))
            pygame.draw.rect(self.pantalla, C_ORO,
                             (x, y - NOMBRE_H + 2, NOMBRE_W, NOMBRE_H), 2, border_radius=3)
            for nx in [x+8, x+NOMBRE_W-8]:
                ny2 = y - NOMBRE_H//2 + 2
                pts = [(nx, ny2-4), (nx+4, ny2), (nx, ny2+4), (nx-4, ny2)]
                pygame.draw.polygon(self.pantalla, C_ORO_CLARO, pts)
            sn = self.f_nombre.render(f"✦  {nombre.upper()}  ✦", True, C_ORO_CLARO)
            self.pantalla.blit(sn, (x+18, y - NOMBRE_H + 6))

        self._wrap_texto(texto_visible, x+24, y+14, w-48, h-30, self.f_texto, C_PERGAMINO)

        if not self._tw_completo:
            cursor_vis = (pygame.time.get_ticks() // 250) % 2 == 0
            if cursor_vis:
                lineas = self._calcular_lineas(texto_visible, w-48)
                if lineas:
                    ultima = lineas[-1]
                    sep = self.f_texto.get_linesize() + 3
                    idx_linea = min(len(lineas) - 1, (h-30)//sep - 1)
                    cx_cur = x+24 + self.f_texto.size(ultima)[0] + 2
                    cy_cur = y+14 + idx_linea * sep
                    pygame.draw.rect(self.pantalla, C_ORO_CLARO,
                                     (cx_cur, cy_cur + 2, 2, self.f_texto.get_linesize() - 2))

        if self._tw_completo and (pygame.time.get_ticks() // 500) % 2 == 0:
            ind = self.f_label.render("▼  ESPACIO / ENTER  para continuar", True, C_ORO_OSC)
            self.pantalla.blit(ind, (x + w - ind.get_width() - 18, y + h - 18))

    # ══════════════════════════════════════════════════════
    #  WORD WRAP
    # ══════════════════════════════════════════════════════
    def _calcular_lineas(self, texto, max_w):
        lineas_raw = texto.split("\n")
        lineas = []
        for raw in lineas_raw:
            if not raw.strip():
                lineas.append("")
                continue
            palabras = raw.split(" ")
            actual = ""
            for p in palabras:
                prueba = (actual + " " + p).strip()
                if self.f_texto.size(prueba)[0] <= max_w:
                    actual = prueba
                else:
                    if actual:
                        lineas.append(actual)
                    actual = p
            if actual:
                lineas.append(actual)
        return lineas

    def _wrap_texto(self, texto, x, y, max_w, max_h, fuente, color):
        lineas = self._calcular_lineas(texto, max_w)
        sep = fuente.get_linesize() + 3
        for i, l in enumerate(lineas):
            if i * sep > max_h - sep:
                break
            if l:
                sh = fuente.render(l, True, C_SOMBRA)
                self.pantalla.blit(sh, (x+1, y + i*sep + 1))
                sf = fuente.render(l, True, color)
                self.pantalla.blit(sf, (x, y + i*sep))

    # ══════════════════════════════════════════════════════
    #  BANNER DE CAPÍTULO
    # ══════════════════════════════════════════════════════
    def _banner(self, cap, titulo, sub=""):
        for alpha in range(0, 245, 10):
            self._dibujar_fondo()
            self._capa_oscura(170)
            pw, ph = 700, 150
            px, py = ANCHO//2 - pw//2, ALTO//2 - ph//2
            pan = pygame.Surface((pw, ph), pygame.SRCALPHA)
            pan.fill((22, 14, 3, min(alpha, 215)))
            self.pantalla.blit(pan, (px, py))
            pygame.draw.rect(self.pantalla, C_ORO, (px, py, pw, ph), 2, border_radius=6)
            pygame.draw.line(self.pantalla, C_ORO_OSC, (px+20, py+28), (px+pw-20, py+28), 1)
            pygame.draw.line(self.pantalla, C_ORO_OSC, (px+20, py+ph-28), (px+pw-20, py+ph-28), 1)
            for cx2, cy2 in [(px, py), (px+pw, py), (px, py+ph), (px+pw, py+ph)]:
                pts = [(cx2, cy2-7), (cx2+7, cy2), (cx2, cy2+7), (cx2-7, cy2)]
                pygame.draw.polygon(self.pantalla, C_ORO_CLARO, pts)
            cap_s = self.f_cap.render(cap, True, C_ORO_OSC)
            cap_s.set_alpha(alpha)
            self.pantalla.blit(cap_s, cap_s.get_rect(center=(ANCHO//2, ALTO//2 - 42)))
            tit_s = self.f_titulo.render(titulo, True, C_ORO)
            tit_s.set_alpha(alpha)
            self.pantalla.blit(tit_s, tit_s.get_rect(center=(ANCHO//2, ALTO//2)))
            if sub:
                sub_s = self.f_sub.render(sub, True, C_PERGAMINO_OSC)
                sub_s.set_alpha(alpha)
                self.pantalla.blit(sub_s, sub_s.get_rect(center=(ANCHO//2, ALTO//2 + 38)))
            pygame.display.flip()
            self.reloj.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    alpha = 244
        pygame.time.delay(1200)

    # ══════════════════════════════════════════════════════
    #  MENÚ DE ELECCIÓN
    # ══════════════════════════════════════════════════════
    def _dibujar_eleccion(self):
        pregunta = self.opciones_elec[0]
        opciones = self.opciones_elec[1:]
        ov = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 170))
        self.pantalla.blit(ov, (0, 0))
        bh, gap = 42, 10
        total_h = len(opciones) * (bh + gap) + 82
        pw = 700
        px = ANCHO//2 - pw//2
        py = ALTO//2 - total_h//2
        pan = pygame.Surface((pw, total_h), pygame.SRCALPHA)
        pan.fill((22, 14, 3, 230))
        self.pantalla.blit(pan, (px, py))
        pygame.draw.rect(self.pantalla, C_ORO, (px, py, pw, total_h), 2, border_radius=6)
        p_s = self.f_sub.render(f"❓  {pregunta}", True, C_ORO_CLARO)
        self.pantalla.blit(p_s, p_s.get_rect(center=(ANCHO//2, py + 26)))
        pygame.draw.line(self.pantalla, C_ORO_OSC, (px+20, py+46), (px+pw-20, py+46), 1)
        for i, op in enumerate(opciones):
            activo = (i == self.opcion_hover)
            bx = ANCHO//2 - (pw-40)//2
            by = py + 56 + i * (bh + gap)
            bw = pw - 40
            btn = pygame.Surface((bw, bh), pygame.SRCALPHA)
            if activo:
                btn.fill((C_ORO[0], C_ORO[1], C_ORO[2], 220))
            else:
                btn.fill(C_ELEC_INACTIVO)
            self.pantalla.blit(btn, (bx, by))
            pygame.draw.rect(self.pantalla, C_ORO if activo else C_ORO_OSC,
                             (bx, by, bw, bh), 2, border_radius=4)
            color_t = C_TINTA if activo else C_PERGAMINO
            num_s = self.f_elec.render(f"{i+1}.", True, C_ORO if not activo else C_TINTA)
            self.pantalla.blit(num_s, (bx+14, by+10))
            txt_s = self.f_elec.render(op, True, color_t)
            self.pantalla.blit(txt_s, (bx+44, by+10))
            if activo:
                rx, ry = bx+bw-22, by+bh//2
                pts = [(rx, ry-5), (rx+5, ry), (rx, ry+5), (rx-5, ry)]
                pygame.draw.polygon(self.pantalla, C_TINTA, pts)
        nav = self.f_label.render("↑ ↓  mover   •   ENTER / clic  elegir", True, C_ORO_OSC)
        self.pantalla.blit(nav, nav.get_rect(center=(ANCHO//2, py + total_h - 14)))

    # ══════════════════════════════════════════════════════
    #  HELPERS GUIÓN
    # ══════════════════════════════════════════════════════
    def _e(self, nombre, texto):
        return {"tipo": "dialogo", "nombre": nombre, "texto": texto}

    def _b(self, cap, titulo, sub=""):
        return {"tipo": "banner", "cap": cap, "titulo": titulo, "sub": sub}

    def _f(self, ruta):
        return {"tipo": "set_fondo", "ruta": ruta}

    def _m(self, ruta, volumen=0.6):
        return {"tipo": "set_musica", "ruta": ruta, "volumen": volumen}

    def _s(self, ruta, lado="izq", alto=260, ancho=200):
        return {"tipo": "set_sprite", "ruta": ruta, "lado": lado,
                "alto": alto, "ancho": ancho}

    def _el(self, pregunta, opciones, callback):
        return {"tipo": "eleccion", "pregunta": pregunta,
                "opciones": opciones, "callback": callback}

    def _insertar_respuesta(self, nombre, texto):
        self._respuesta_pendiente = {"nombre": nombre, "texto": texto}

    # ══════════════════════════════════════════════════════
    #  GUIÓN COMPLETO
    # ══════════════════════════════════════════════════════
    def _construir_escenas(self):
        E=self._e; B=self._b; F=self._f; M=self._m
        S=self._s; EL=self._el

        def cb1(i):
            self._insertar_respuesta(*[
                ("Atenea",   "Bien hecho, Odiseo. Tu devoción me complace.\nVelaré desde el Olimpo por ti en cada travesía.\n[+2 favor divino, +1 sabiduría]"),
                ("Narrador", "Viertes vino al mar. Una ola enorme te empapa.\nEn el fondo del mar, Poseidón bufa... pero menos.\n[+1 favor divino]"),
                ("Narrador", "Partes sin rezar. Los dioses lo notan.\nLos dioses SIEMPRE lo notan.\n[-1 favor divino]"),
            ][i])

        def cb2(i):
            self._insertar_respuesta(*[
                ("Polifemo",  "¡JA! ¡NADIE! ¡Qué nombre tan raro!\nPues bien, NADIE, por darme este delicioso vino...\nSerás el último en morir."),
                ("Narrador",  "¡ODISEO! ¡El destructor de Troya!\nAhora Poseidón sabe exactamente a quién perseguir.\n[-2 tripulantes]"),
                ("Narrador",  "El silencio no ayudó mucho.\nPolifemo comió a dos hombres antes de que\nse te ocurriera el plan del vino y la estaca.\n[-2 tripulantes]"),
            ][i])

        def cb7(i):
            self._insertar_respuesta(*[
                ("Narrador", "Pasáis por el lado de Escila.\nSeis de tus hombres desaparecen en un instante.\n[-6 tripulantes]"),
                ("Narrador", "Caribdis exhala el agua. Diez segundos.\nNo alcanza. Terminás donde Scylla de todas formas.\n[-6 tripulantes]"),
                ("Narrador", "Escila es inmortal. Las seis cabezas comen el doble.\n[-20 vida, -8 tripulantes]"),
            ][i])

        def cb9(i):
            self._insertar_respuesta(*[
                ("Zeus", "La lealtad a los tuyos es admirable.\nPero tu tripulación ya eligió su destino\nal tocar el ganado sagrado.\nLlegarás a Ítaca... solo."),
                ("Zeus", "El amor fiel es raro entre los mortales.\nPor eso, y solo por eso, te concedo el regreso.\nVe a ella."),
                ("Zeus", "Por el honor de Grecia... tu tripulación nunca volverá.\nEl camino seguirá siendo tuyo. Haz que valga la pena."),
            ][i])

        return [
            # ── CAP I ────────────────────────────────────
            F("fondos/barco_odiseo_orilla_1.jpg"), M("musica/epica.ogg"),
            B("CAPÍTULO I", "La Caída de Troya", "Año décimo de la guerra"),
            E("Narrador", "Han pasado diez años. Troya arde..\nLas llamas iluminan el Egeo entero.\nEl gran caballo de madera, idea de Odiseo,\nselló el destino de la ciudad inexpugnable."),
            S("sprites/odiseo.png", "center", alto=380, ancho=460),
            E("Odiseo", "Diez años de guerra.. Por fin ha terminado.\nHemos sobrevivido.\nAhora solo queda navegar a casa...\n¿Cuánto tiempo tardaré en volver a Ithaca?"),
            EL("Antes de zarpar, ¿qué hacés?",
               ["Rezás a Atenea pidiendo protección",
                "Hacés una ofrenda a Poseidón por si acaso",
                "Partís de inmediato, sin perder tiempo"], cb1),

            # ── CAP II ───────────────────────────────────
            F("fondos/cueva_polifemo.jpg"), M("musica/tension.ogg"),
            B("CAPÍTULO II", "La Isla del Cíclope", "Polifemo, hijo de Poseidón"),
            E("Narrador", "Primera parada: la isla de los Cíclopes.\nUna cueva enorme. Jugosas y peludas ovejas.\nHuesos del tamaño de árboles.\nTodo esto son señales de peligro muy claras."),
            E("Narrador", "Tus compañeros, hambrientos luego del viaje,\nmataron a una de las ovejas de la cueva."),
            S("sprites/ciclope.png", "center", alto=390, ancho=560),
            E("Polifemo", "¡¡FORASTEROS!! ¿QUÉ HACEN EN MI CUEVA?\n¡Mataron.... a mi oveja!"),
            E("Polifemo", "A mi oveja...\nfavorita..."),
            S("sprites/odiseo.png", "izq", alto=380, ancho=460),
            EL("Polifemo pregunta tu nombre. ¿Qué respondés?",
               ["Mi nombre es NADIE, gran Polifemo.. (le ofrecés vino)",
                "Soy Odiseo, rey de Ítaca.",
                "No digo nada."], cb2),
            E("Narrador", "Le das vino. Mucho vino.\nEl cíclope bebe y bebe hasta saciarse.\nEmpieza la batalla."),

            # ── CAP II.I ─────────────────────────────────
            F("fondos/castillo_eolus.jpg"), M("musica/viento.ogg"),
            B("CAPÍTULO II.I", "La Isla Flotante de Eolia", "El regalo del viento — y la traición"),
            S("sprites/eolus.png", "center", alto=380, ancho=460),
            E("Eolus", "¡Odiseo! ¡El gran héroe de Troya! Bienvenido.\nTengo un regalo: este saco de cuero.\nLo único que no debés hacer es... abrirlo."),
            S("sprites/odiseo.png", "izq", alto=380, ancho=460),
            E("Narrador", "Con el viento del oeste soplando sin parar,\nen diez días veis Ítaca en el horizonte.\nTAN CERCA. Y entonces... Odiseo se queda dormido."),
            S("sprites/bolso.png", "center", alto=280, ancho=360),
            E("Tripulante", "Psst... ¿qué habrá en ese saco?\nSeguro son tesoros. Odiseo se los guarda para él.\n¿Y si lo abrimos? Solo un vistazo..."),
            S("sprites/ministorm.png", "center", alto=280, ancho=360),
            E("Narrador", "ABREN EL SACO.\n\nTodos los vientos del mundo estallan a la vez.\nLa tormenta más colosal del Mediterráneo."),
            S("sprites/odiseo.png", "center", alto=380, ancho=460),
            E("Odiseo", "No. No, no, no...\n¿POR QUÉ ABRIERON EL SACO?"),
            S("sprites/eolus.png", "center", alto=380, ancho=460),
            E("Eolus", "...Abrieron el saco, ¿verdad?\nNo puedo ayudarte de nuevo. Lo siento.\nClaramente los dioses te odian."),

            # ── CAP III ──────────────────────────────────
            F("fondos/escena_abre_la_bolsa.jpg"), M("musica/tormenta.ogg"),
            B("CAPÍTULO III", "La Maldición de Poseidón", "El dios desencadena su furia"),
            S("sprites/poseidon.png", "center", alto=380, ancho=460),
            E("Narrador", "Gracias al gran poder del saco de Eolus.\nLa tormenta los llevó a la boca de uno de los dioses.\nMás peligrosos."),
            E("Poseidón", "Poseidón, al fin te encuentro...\n¡Cegaste a mi hijo y ahora el mar es tu prisión!\n¡Voy a desatar la tormenta más terrible\nque ningún barco haya sobrevivido jamás!"),
            # ← MiniJuego2().jugar()
            E("Narrador", "Sobreviviste... apenas.\nPoseidón se calmó por ahora, pero volverá."),

            # ── CAP IV ───────────────────────────────────
            F("fondos/palacio_circe2.jpg"), M("musica/misterio.ogg"),
            B("CAPÍTULO IV", "La Isla de Eea", "La ninfa Circe convierte en cerdos a los hombres"),
            S("sprites/odiseo.png", "izq", alto=380, ancho=460),
            E("Narrador", "Acabaron en la isla de Eea. Hermosa. Sospechosamente hermosa..\nEncuentran un palacio donde una mujer divina canta,\nrodeada de lobos y leones... muy dóciles."),
            F("fondos/palacio_circe.jpg"),
            S("sprites/circe.png", "center", alto=390, ancho=460),
            E("Circe", "¡Bienvenidos, viajeros! Pasen, pasen..\nTengo vino, queso, carne asada...\n¡Un festín digno de reyes! ♡"),
            E("Narrador", "Los hombres comen y beben sin sospechar nada.\n*POOF*\nTus hombres ahora son cerdos muy confundidos."),
            S("sprites/hermes.png", "center", alto=380, ancho=460),
            E("Hermes", "¡Odiseo! (El dios Hermes aparece para brindarte ayuda)\nAntes de entrar, tomá esta hierba.\nSe llama moly. Neutraliza los hechizos de Circe."),
            S("sprites/circe.png", "center", alto=390, ancho=460),
            E("Circe", "¡Im...posible! Resististe mi hechizo.\nEres el primero en siglos, bueno,\nveremos cuánto perdura."),
            # ← MiniJuego3().jugar()

            # ── CAP V ────────────────────────────────────
            F("fondos/inframundo_teresias.jpg"), M("musica/inframundo.ogg"),
            B("CAPÍTULO V", "El Inframundo", "Consulta al profeta Tiresias"),
            S("sprites/circe.png", "der"),
            E("Circe", "(Circe acepta ayudarles)\nPara saber cómo regresar a Ítaca,\ndebes visitar el Hades.\nSolo el profeta Tiresias conoce el camino."),
            E("Narrador", "El Hades. El mundo de los muertos.\nEl lugar al que nadie quiere ir\ny del que nadie debería volver.\nOdiseo está aquí de visita. Con cita previa."),
            S("sprites/tiresias.png", "center", alto=380, ancho=460),
            E("Tiresias", "Odiseo... te estaba esperando.\nEl olor de los vivos aquí es perturbador."),
            E("Tiresias", "Escuchame bien. La isla de Trinacia.\nEl ganado sagrado de Helios.\nNO. LO. TOQUES."),
            E("Tiresias", "El futuro.. Veo traiciones.\nVeo el sacrificio de hombres.\nVeo a un hombre que logra regresar a casa con vida.\nPero ya no eres tú."),
            S("sprites/narrador.png", "izq"),
            E("Narrador", "También encontrás la sombra de tu madre.\nNo sabías que había muerto.\nMurió de pena esperándote.\n\nIntentás abrazarla. Las sombras no se abrazan."),

            # ── CAP VI ───────────────────────────────────
            F("fondos/escena_sirenas.jpg"), M("musica/sirenas.ogg"),
            B("CAPÍTULO VI", "Las Sirenas", "La música que mata"),
            E("Narrador", "Su música es tan hermosa que cualquier marinero\ndirige el barco hacia las rocas sin poder evitarlo.\nNo importa cuánto ames a tu familia."),
            E("Narrador", "Tapás los oídos de todos con cera de abeja.\nPero la única forma de huir de Poseidón\nsería atravesando el valle de SCYLLA."),

            # ── CAP VII ──────────────────────────────────
            F("fondos/scylla.jpg"), M("musica/peligro.ogg"),
            B("CAPÍTULO VII", "Scylla", "El monstruo marino de seis cabezas"),
            E("Narrador", "A un lado: SCYLLA. Seis cabezas. Doce patas.\nCome marineros de aperitivo.\nAl otro lado: CARIBDIS, un remolino que\nengulle barcos enteros tres veces al día."),
            E("Narrador", "No hay paso seguro, Odiseo.\nEscila tomará seis hombres, uno por cabeza.\nCaribdis podría tomar el barco entero."),
            S("sprites/scylla.png", "center", alto=380, ancho=460),
            EL("¿Por dónde pasás el barco?",
               ["Por Scylla — perdés hombres pero el barco sobrevive.",
                "Por Caribdis — si el timing es perfecto...",
                "Atacás a Scylla con todas tus flechas."], cb7),
            S("sprites/odiseo.png", "center", alto=380, ancho=460),
            E("Tripulante", "Odiseo, ¿por qué pediste que huyamos?\nPerdimos hombres.. y ni siquiera peleamos.\nTú ya lo sabías, ¿no? Nos traicionaste...."),
            # ← MiniJuego4().jugar()

            # ── CAP VIII ─────────────────────────────────
            F("fondos/isla_helios.jpg"), M("musica/misterio.ogg"),
            B("CAPÍTULO VIII", "El Ganado de Helios", "La prueba más difícil del viaje"),
            E("Narrador", "Luego de una gran batalla, a pesar de que ganaste,\ntu tripulación acabó noqueandote,\nY te despertaste atado en la isla del dios del sol."),
            S("sprites/estatua_helios.png", "center", alto=380, ancho=460),
            E("Narrador", "La isla de Trinacia. El ganado sagrado de Helios\npasta tranquilamente en los campos verdes.\nTiresias fue explícito: 'NO LAS TOQUES'.\nPero una tormenta os mantiene varados semanas."),
            S("sprites/estatua_helios2.png", "center", alto=380, ancho=460),
            E("Narrador", "Las vacas son sacrificadas y comidas.\nEsa noche las pieles se levantan. La carne muge.\nAl zarpar, Zeus lanza su rayo sobre el barco.\n*CRAAAAASH*\nToda la tripulación perece en el mar."),

            # ── CAP IX ───────────────────────────────────
            F("fondos/camarote_barco.jpg"), M("musica/olimpo.ogg"),
            B("CAPÍTULO IX", "Zeus Hace Elegir", "¿Tripulación o esposa?"),
            S("sprites/zeus.png", "center", alto=380, ancho=460),
            E("Narrador", "Zeus apareció.\nAl cometer asesinato de las amigas del dios del sol\nel dios pidió ayuda a Zeus."),
            E("Zeus", "Tu tripulación cometió sacrilegios contra Helios.\nLa justicia divina exige consecuencias.\nPero Atenea intercede por vos sin descanso."),
            S("sprites/atenea.png", "izq"),
            E("Atenea", "(La diosa aparece en forma de su animal elemental)\n¡Padre Zeus, Odiseo ha sufrido suficiente!\n13 años lejos de casa. ¡Merece volver!"),
            S("sprites/odiseo.png", "center", alto=380, ancho=460),
            EL("Zeus te pregunta: ¿Qué es lo más importante para tí?",
               ["Mi tripulación — nunca los abandonaré",
                "Volver con Penélope — es mi razón de vivir",
                "El honor de Grecia — lo que sea mejor para todos"], cb9),

            # ── CAP X ────────────────────────────────────
            F("fondos/entrada_isla_calypso.jpg"), M("musica/nostalgia.ogg"),
            B("CAPÍTULO X", "Escapa de Calipso", "Siete años prisionero en la isla de Ogigia"),
            S("sprites/calypso.png", "center", alto=380, ancho=460),
            E("Calipso", "Odiseo, aquí estás a salvo. Yo te cuido.\nYo te quiero. ¿Para qué regresar?\nPenélope envejece. Yo soy inmortal.\nPodría hacerte inmortal también."),
            E("Narrador", "Luego de todos los problemas pasados, despertaste en una isla\ncon una única mujer\nque resultó ser una ninfa que te retuvo por 7 años\nporque hasta que llegaste, ella estaba sola allí."),
            S("sprites/odiseo.png", "center", alto=380, ancho=460),
            E("Odiseo", "*sentado en la orilla mirando el horizonte*\nCada día miro el mar en dirección a Ítaca.\nCada día lloro.\nQuiero volver a casa."),
            S("sprites/atenea.png", "izq", alto=180, ancho=460),
            E("Narrador", "Atenea decide pedirle a Zeus una intervención divina.\nSiete años. Un paraíso que se siente\ncomo una prisión dorada."),

            # ── CAP XI ───────────────────────────────────
            F("fondos/templo.jpg"), M("musica/olimpo.ogg"),
            B("CAPÍTULO XI", "Atenea vs Zeus", "La batalla de argumentos en el Olimpo"),
            S("sprites/atenea.png", "izq"),
            E("Atenea", "Padre Zeus, Odiseo ya ha sufrido bastante.\nCalipso lo retuvo siete años.\nPoseidón lo persigue sin descanso.\n¡Es hora de que regrese a casa!"),
            S("sprites/zeus.png", "der", alto=380, ancho=460),
            E("Zeus", "Atenea, hija mía. Poseidón tiene sus razones.\nNecesito argumentos sólidos para decidir."),
            # ← MiniJuego5().jugar()
            E("Zeus", "...Bien. Atenea tiene razón.\nEnviaré a Hermes a ordenar a Calipso\nque libere a Odiseo."),

            # ── CAP XII ──────────────────────────────────
            F("fondos/pelea_poseidon.jpg"), M("musica/tormenta.ogg"),
            B("CAPÍTULO XII", "Poseidón Pelea", "La tormenta final antes de Ítaca"),
            S("sprites/poseidon.png", "center", alto=380, ancho=460),
            E("Poseidón", "¿QUÉ? ¡Zeus cedió ante Atenea!\n¡NO MIENTRAS YO EXISTA!\n¡Te daré la tormenta FINAL!"),
            S("sprites/odiseo.png", "center", alto=380, ancho=460),
            E("Narrador", "En la balsa, a días de la costa de los feacios,\nPoseidón desata su tormenta más colosal.\nEs ahora o nunca."),
            # ← MiniJuego6().jugar()
            E("Narrador", "Odiseo navega por dos días\nhasta llegar exhausto a la isla de los feacios."),

            # ── CAP XIII ─────────────────────────────────
            F("fondos/castillo_odi.jpg"), M("musica/regreso.ogg"),
            B("CAPÍTULO XIII", "Regreso a Ítaca", "El rey mendigo — lucha contra los pretendientes"),
            S("sprites/narrador.png", "izq"),
            E("Narrador", "Ítaca. Veinte años después.\nOdiseo disfrazado de viejo mendigo.\nEn el palacio hay 108 pretendientes.\nComen su comida. Beben su vino. Esperan que esté muerto."),
            E("Narrador", "Tu viejo perro Argos te reconoce al llegar.\nMueve la cola. Luego cierra los ojos para siempre.\nTe esperó veinte años para verte regresar.\n..."),
            S("sprites/atenea.png", "der"),
            E("Atenea", "Penélope ha prometido casarse\ncon quien pueda pasar una flecha por doce hachas\nusando el gran arco de Odiseo.\nNadie ha podido tensarlo siquiera."),
            S("sprites/odiseo.png", "izq"),
            E("Odiseo", "*(tensa el arco con facilidad)*\n*(la flecha pasa por las doce hachas)*\n*(silencio total en el salón)*\n\n...La competición ha terminado."),
            S("sprites/narrador.png", "izq"),
            E("Narrador", "Los pretendientes se dan cuenta. Ya es tarde.\nOdiseo ha vuelto. Y el gran arco apunta\ndirecto hacia ellos."),
            # ← MiniJuegoFinal7().jugar()
            E("Narrador", "¡Los pretendientes caen uno a uno!\nTelémaco lucha junto a su padre.\n¡ÍTACA ES TUYA!\n[+20 moral, +2 favor divino]"),

            # ── CAP XIV ──────────────────────────────────
            F("fondos/escena_penelope.jpg"), M("musica/reencuentro.ogg"),
            B("CAPÍTULO XIV", "Finalmente con Penélope", "El reencuentro después de veinte años"),
            S("sprites/narrador.png", "izq"),
            E("Narrador", "El palacio está tranquilo.\nTelémaco abraza a su padre por primera vez\nen veinte años. Ambos lloran sin avergonzarse."),
            E("Narrador", "Y entonces... Penélope baja las escaleras."),
            S("sprites/penelope.png", "der", alto=380, ancho=460),
            E("Penélope", "Me dicen que mi esposo ha regresado.\nPero he esperado veinte años.\nHe aprendido a no hacerme ilusiones fácilmente."),
            S("sprites/odismile.png", "izq", alto=380, ancho=460),
            E("Odiseo", "Penélope... nuestra cama.\nLa tallé yo mismo en el tronco de un olivo vivo.\nLa cama no se puede mover.\nNadie puede saberlo excepto tú y yo."),
            S("sprites/penelope2.png", "center", alto=380, ancho=460),
            E("Penélope", "*(pausa muy larga)*\n\n...La cama.\nSolo tú podías saber eso.\n\n*(voz quebrada)*\n\nOdiseo."),
            S("sprites/odismile.png", "center", alto=380, ancho=460),
            E("Odiseo", "Penélope."),
            E("Narrador", "Veinte años. Una guerra. Dioses furiosos.\nMonstruos. Hechiceras. Tormentas. El inframundo.\nSiete años prisionero. Una batalla en el palacio.\n\nY al final... dos personas que nunca dejaron\nde esperarse."),
            S("sprites/penelope.png", "der", alto=380, ancho=460),
            E("Penélope", "Veinte años tarde."),
            S("sprites/odiseo.png", "izq", alto=380, ancho=460),
            E("Odiseo", "El mar es complicado."),
            S(None),
            F("fondos/final.png"),
            E("Narrador", "Y así termina la odisea más larga de la historia.\nOdiseo, el más astuto de todos los héroes,\nfinalmente llegó a casa.\n\n                    — FIN —"),
        ]

    # ══════════════════════════════════════════════════════
    #  SETUP DE ESCENA
    # ══════════════════════════════════════════════════════
    def _setup(self, esc):
        t = esc["tipo"]
        if t == "set_fondo":
            r = esc["ruta"]
            if r not in self._fondos:
                self._fondos[r] = cargar_imagen(r, (ANCHO, ALTO), alpha=False)
            self.fondo_actual = self._fondos[r]
            return "skip"
        if t == "set_musica":
            if cargar_musica(esc["ruta"]):
                pygame.mixer.music.set_volume(esc.get("volumen", 0.6))
                pygame.mixer.music.play(-1)
            return "skip"
        if t == "set_sprite":
            ruta = esc["ruta"]
            if ruta is None:
                self.sprite_actual = None
            else:
                alto_max  = esc.get("alto",  SPRITE_ALTO)
                ancho_max = esc.get("ancho", SPRITE_ANCHO)
                cache_key = (ruta, alto_max, ancho_max)
                if cache_key not in self._sprites:
                    self._sprites[cache_key] = cargar_imagen_proporcional(ruta, alto_max, ancho_max)
                self.sprite_actual = self._sprites[cache_key]
                self.sprite_lado   = esc.get("lado", "izq")
            return "skip"
        if t == "banner":
            self._banner(esc["cap"], esc["titulo"], esc.get("sub", ""))
            return "skip"
        if t == "dialogo":
            self._tw_iniciar(esc["texto"])
            return "dialogo"
        if t == "eleccion":
            self.opciones_elec = [esc["pregunta"]] + esc["opciones"]
            self.opcion_hover  = 0
            self._respuesta_pendiente = None
            return "eleccion"
        return "skip"

    # ══════════════════════════════════════════════════════
    #  PANTALLA DE TÍTULO
    # ══════════════════════════════════════════════════════
    def _pantalla_titulo(self):
        fondo_titulo = cargar_imagen("fondos/barco_odiseo_orilla_1.jpg", (ANCHO, ALTO), alpha=False)
        tick = 0
        seleccion = 0
        opciones  = ["  INICIAR JUEGO  ", "      SALIR      "]
        reloj_intro = pygame.time.Clock()

        while True:
            reloj_intro.tick(FPS)
            tick += 1

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_UP, pygame.K_w):
                        seleccion = (seleccion - 1) % len(opciones)
                    if ev.key in (pygame.K_DOWN, pygame.K_s):
                        seleccion = (seleccion + 1) % len(opciones)
                    if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if seleccion == 0:
                            return
                        else:
                            pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEMOTION:
                    for i in range(len(opciones)):
                        bx = ANCHO//2 - 160
                        by = ALTO//2 + 60 + i * 58
                        if bx <= ev.pos[0] <= bx+320 and by <= ev.pos[1] <= by+44:
                            seleccion = i
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(opciones)):
                        bx = ANCHO//2 - 160
                        by = ALTO//2 + 60 + i * 58
                        if bx <= ev.pos[0] <= bx+320 and by <= ev.pos[1] <= by+44:
                            if i == 0:
                                return
                            else:
                                pygame.quit(); sys.exit()

            # Dibujo
            if fondo_titulo:
                self.pantalla.blit(fondo_titulo, (0, 0))
            else:
                self.pantalla.fill(C_FONDO_BASE)

            ov = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 155))
            self.pantalla.blit(ov, (0, 0))

            for ly in [ALTO//2 - 110, ALTO//2 + 52]:
                pygame.draw.line(self.pantalla, C_ORO_OSC, (60, ly), (ANCHO-60, ly), 1)

            sub_top = self.f_cap.render("✦  VelvetProyect  ✦", True, C_ORO_OSC)
            self.pantalla.blit(sub_top, sub_top.get_rect(center=(ANCHO//2, ALTO//2 - 128)))

            pulso = 0.85 + 0.15 * math.sin(tick * 0.05)
            color_titulo = (int(C_ORO[0]*pulso), int(C_ORO[1]*pulso), int(C_ORO[2]*pulso*0.6))
            f_grande = pygame.font.SysFont("Times New Roman", 62, bold=True)
            tit_s = f_grande.render("LA ODISEA", True, (0, 0, 0))
            tit   = f_grande.render("LA ODISEA", True, color_titulo)
            self.pantalla.blit(tit_s, tit_s.get_rect(center=(ANCHO//2+3, ALTO//2-62+3)))
            self.pantalla.blit(tit,   tit.get_rect(center=(ANCHO//2,     ALTO//2-62)))

            sub = self.f_sub.render("La historia de Odiseo, Rey de Ítaca", True, C_PERGAMINO_OSC)
            self.pantalla.blit(sub, sub.get_rect(center=(ANCHO//2, ALTO//2 - 14)))

            for dx in [-290, 290]:
                cx2 = ANCHO//2 + dx
                cy2 = ALTO//2 - 62
                p = 8 if tick % 30 < 15 else 6
                pts = [(cx2, cy2-p),(cx2+p,cy2),(cx2,cy2+p),(cx2-p,cy2)]
                pygame.draw.polygon(self.pantalla, C_ORO, pts)

            bw, bh = 320, 44
            for i, texto in enumerate(opciones):
                activo = (i == seleccion)
                bx = ANCHO//2 - bw//2
                by = ALTO//2 + 60 + i * 58
                btn = pygame.Surface((bw, bh), pygame.SRCALPHA)
                btn.fill((C_ORO[0], C_ORO[1], C_ORO[2], 210) if activo else (22, 14, 3, 200))
                self.pantalla.blit(btn, (bx, by))
                pygame.draw.rect(self.pantalla, C_ORO if activo else C_ORO_OSC,
                                 (bx, by, bw, bh), 2, border_radius=5)
                if activo:
                    for rx2 in [bx+12, bx+bw-12]:
                        ry2 = by + bh//2
                        pts = [(rx2,ry2-5),(rx2+5,ry2),(rx2,ry2+5),(rx2-5,ry2)]
                        pygame.draw.polygon(self.pantalla, C_TINTA, pts)
                color_t = C_TINTA if activo else C_PERGAMINO
                txt = self.f_elec.render(texto, True, color_t)
                self.pantalla.blit(txt, txt.get_rect(center=(ANCHO//2, by + bh//2)))

            inst = self.f_label.render("↑ ↓  navegar   •   ENTER / clic  confirmar", True, C_ORO_OSC)
            self.pantalla.blit(inst, inst.get_rect(center=(ANCHO//2, ALTO - 22)))

            pygame.display.flip()

    # ══════════════════════════════════════════════════════
    #  BUCLE PRINCIPAL
    # ══════════════════════════════════════════════════════
    def correr(self):
        self._pantalla_titulo()
        self._respuesta_pendiente = None
        while self.escena_idx < len(self.escenas):
            esc  = self.escenas[self.escena_idx]
            modo = self._setup(esc)

            if modo == "skip":
                self.escena_idx += 1
                continue

            if modo == "dialogo":
                loop = True
                while loop:
                    self.reloj.tick(FPS)
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit(); sys.exit()
                        if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_SPACE, pygame.K_RETURN):
                            if not self._tw_completo:
                                self._tw_saltar()
                            else:
                                loop = False
                        if ev.type == pygame.MOUSEBUTTONDOWN:
                            if not self._tw_completo:
                                self._tw_saltar()
                            else:
                                loop = False
                    self._tw_actualizar()
                    texto_visible = self._tw_texto_total[:self._tw_chars_vis]
                    self._dibujar_fondo()
                    self._capa_oscura(80)
                    self._dibujar_sprite()
                    self._dibujar_caja(esc.get("nombre", ""), texto_visible)
                    pygame.display.flip()

                self.escena_idx += 1
                if self._respuesta_pendiente:
                    rp = self._respuesta_pendiente; self._respuesta_pendiente = None
                    self.escenas.insert(self.escena_idx, self._e(rp["nombre"], rp["texto"]))

            elif modo == "eleccion":
                opciones = esc["opciones"]
                loop = True
                while loop:
                    self.reloj.tick(FPS)
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit(); sys.exit()
                        if ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_UP:
                                self.opcion_hover = (self.opcion_hover - 1) % len(opciones)
                            if ev.key == pygame.K_DOWN:
                                self.opcion_hover = (self.opcion_hover + 1) % len(opciones)
                            if ev.key == pygame.K_RETURN:
                                esc["callback"](self.opcion_hover); loop = False
                        if ev.type == pygame.MOUSEMOTION:
                            bh = 42
                            for i in range(len(opciones)):
                                by = ALTO//2 - (len(opciones)*(bh+10))//2 + i*(bh+10)
                                if ANCHO//2-330 <= ev.pos[0] <= ANCHO//2+330 and by <= ev.pos[1] <= by+bh:
                                    self.opcion_hover = i
                        if ev.type == pygame.MOUSEBUTTONDOWN:
                            bh = 42
                            for i in range(len(opciones)):
                                by = ALTO//2 - (len(opciones)*(bh+10))//2 + i*(bh+10)
                                if ANCHO//2-330 <= ev.pos[0] <= ANCHO//2+330 and by <= ev.pos[1] <= by+bh:
                                    self.opcion_hover = i
                                    esc["callback"](self.opcion_hover); loop = False
                    self._dibujar_fondo()
                    self._capa_oscura(80)
                    self._dibujar_sprite()
                    self._dibujar_eleccion()
                    pygame.display.flip()

                self.escena_idx += 1
                if self._respuesta_pendiente:
                    rp = self._respuesta_pendiente; self._respuesta_pendiente = None
                    self.escenas.insert(self.escena_idx, self._e(rp["nombre"], rp["texto"]))

        self._pantalla_fin()
        pygame.quit()

    # ══════════════════════════════════════════════════════
    #  PANTALLA FINAL
    # ══════════════════════════════════════════════════════
    def _pantalla_fin(self):
        pygame.mixer.music.fadeout(2000)
        for alpha in range(0, 256, 5):
            self._dibujar_fondo()
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            s.fill((0, 0, 0, alpha))
            self.pantalla.blit(s, (0, 0))
            t = self.f_titulo.render("— FIN —", True, C_ORO)
            t.set_alpha(alpha)
            self.pantalla.blit(t, t.get_rect(center=(ANCHO//2, ALTO//2)))
            pygame.display.flip()
            self.reloj.tick(FPS)
        pygame.time.delay(3500)


# ══════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    novela = NovelVisual()
    novela.correr()