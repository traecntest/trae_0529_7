import math
import random

from PySide6.QtCore import QTimer, Qt, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QRadialGradient, QLinearGradient, QPainterPath
from PySide6.QtWidgets import QWidget


CYAN = "#00FFFF"
MAGENTA = "#FF00FF"
BLUE = "#0088FF"
ORANGE = "#FF8800"
PURPLE = "#8800FF"

RUNIC_SYMBOLS = [
    "ᚠ", "ᚢ", "ᚦ", "ᚨ", "ᚱ", "ᚲ", "ᚷ", "ᚹ",
    "ᚺ", "ᚾ", "ᛁ", "ᛃ", "ᛇ", "ᛈ", "ᛉ", "ᛊ",
    "ᛏ", "ᛒ", "ᛖ", "ᛗ", "ᛚ", "ᛜ", "ᛞ", "ᛟ",
]


class MagicCircleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0.0
        self._ring_speeds = [1.0, -0.6, 0.4, -0.3, 0.8]
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def _tick(self):
        self._angle += 1.0
        if self._angle >= 360.0:
            self._angle -= 360.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        base_r = min(cx, cy) * 0.9

        for idx, speed in enumerate(self._ring_speeds):
            ring_angle = self._angle * speed
            ring_r = base_r * (0.3 + idx * 0.15)
            self._draw_ring(painter, cx, cy, ring_r, ring_angle, idx)

        self._draw_center_star(painter, cx, cy, base_r * 0.18, self._angle * 0.5)
        painter.end()

    def _draw_ring(self, painter, cx, cy, radius, angle_deg, index):
        colors = [CYAN, BLUE, PURPLE, MAGENTA, CYAN]
        color = QColor(colors[index % len(colors)])
        color.setAlpha(160)

        pen = QPen(color, 1.5)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        painter.save()
        painter.translate(cx, cy)
        painter.rotate(angle_deg)

        painter.drawEllipse(int(-radius), int(-radius), int(2 * radius), int(2 * radius))

        inner_r = radius * 0.88
        painter.drawEllipse(int(-inner_r), int(-inner_r), int(2 * inner_r), int(2 * inner_r))

        dash_color = QColor(colors[index % len(colors)])
        dash_color.setAlpha(80)
        dash_pen = QPen(dash_color, 0.8, Qt.DashLine)
        painter.setPen(dash_pen)
        mid_r = radius * 0.94
        painter.drawEllipse(int(-mid_r), int(-mid_r), int(2 * mid_r), int(2 * mid_r))

        fill_color = QColor(colors[index % len(colors)])
        fill_color.setAlpha(12)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(fill_color))
        painter.drawEllipse(int(-radius), int(-radius), int(2 * radius), int(2 * radius))

        painter.setPen(pen)
        sides = 6 + index * 2
        painter.drawPolygon(self._regular_polygon(0, 0, radius * 0.82, sides))

        symbol_count = min(8 + index * 2, len(RUNIC_SYMBOLS))
        symbol_r = radius * 0.91
        font = QFont("Segoe UI Symbol", max(8, int(radius * 0.1)))
        font.setBold(True)
        painter.setFont(font)
        text_color = QColor(colors[index % len(colors)])
        text_color.setAlpha(200)
        painter.setPen(text_color)
        for i in range(symbol_count):
            a = (2.0 * math.pi * i) / symbol_count
            sx = symbol_r * math.cos(a)
            sy = symbol_r * math.sin(a)
            painter.drawText(int(sx) - 5, int(sy) + 5, RUNIC_SYMBOLS[i % len(RUNIC_SYMBOLS)])

        tick_color = QColor(colors[index % len(colors)])
        tick_color.setAlpha(120)
        painter.setPen(QPen(tick_color, 1.0))
        for i in range(symbol_count * 2):
            a = (2.0 * math.pi * i) / (symbol_count * 2)
            x1 = radius * 0.85 * math.cos(a)
            y1 = radius * 0.85 * math.sin(a)
            x2 = radius * math.cos(a)
            y2 = radius * math.sin(a)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        painter.restore()

    def _draw_center_star(self, painter, cx, cy, radius, angle_deg):
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(angle_deg)

        glow = QRadialGradient(0, 0, radius * 1.5)
        glow.setColorAt(0.0, QColor(CYAN))
        glow.setColorAt(0.5, QColor(BLUE))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(glow))
        painter.drawEllipse(int(-radius * 1.5), int(-radius * 1.5), int(3 * int(radius * 1.5)), int(3 * int(radius * 1.5)))

        star_color = QColor(CYAN)
        star_color.setAlpha(180)
        painter.setPen(QPen(star_color, 1.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon(self._regular_polygon(0, 0, radius, 5))

        painter.rotate(36.0)
        inner_color = QColor(MAGENTA)
        inner_color.setAlpha(140)
        painter.setPen(QPen(inner_color, 1.0))
        painter.drawPolygon(self._regular_polygon(0, 0, radius * 0.55, 5))

        painter.restore()

    @staticmethod
    def _regular_polygon(cx, cy, radius, sides):
        from PySide6.QtGui import QPolygonF
        polygon = QPolygonF()
        for i in range(sides):
            angle = (2.0 * math.pi * i) / sides - math.pi / 2.0
            polygon.append(QPointF(cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
        return polygon

    def __del__(self):
        if hasattr(self, "_timer"):
            self._timer.stop()


class ParticleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._particles = []
        self._init_particles(50)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def _init_particles(self, count):
        for _ in range(count):
            self._particles.append(self._new_particle())

    def _new_particle(self, at_bottom=False):
        x = random.uniform(0, max(self.width(), 400))
        y = random.uniform(0, max(self.height(), 400)) if not at_bottom else max(self.height(), 400)
        size = random.uniform(2.0, 6.0)
        speed = random.uniform(0.3, 1.2)
        drift = random.uniform(-0.3, 0.3)
        alpha = random.randint(80, 220)
        color_choice = random.choice([CYAN, MAGENTA, BLUE, PURPLE])
        return {
            "x": x, "y": y, "size": size, "speed": speed,
            "drift": drift, "alpha": alpha, "color": color_choice,
        }

    def _tick(self):
        for i, p in enumerate(self._particles):
            p["y"] -= p["speed"]
            p["x"] += p["drift"]
            p["alpha"] = max(0, p["alpha"] - 1)
            if p["y"] < -10 or p["alpha"] <= 0:
                self._particles[i] = self._new_particle(at_bottom=True)
                self._particles[i]["y"] = max(self.height(), 400)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        for p in self._particles:
            color = QColor(p["color"])
            color.setAlpha(p["alpha"])
            gradient = QRadialGradient(p["x"], p["y"], p["size"] * 2.0)
            gradient.setColorAt(0.0, color)
            color_outer = QColor(p["color"])
            color_outer.setAlpha(0)
            gradient.setColorAt(1.0, color_outer)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(gradient))
            size = p["size"] * 4.0
            painter.drawEllipse(int(p["x"] - size / 2), int(p["y"] - size / 2), int(size), int(size))
            core_color = QColor(p["color"])
            core_color.setAlpha(min(255, p["alpha"] + 50))
            painter.setBrush(QBrush(core_color))
            painter.drawEllipse(int(p["x"] - p["size"] / 2), int(p["y"] - p["size"] / 2), int(p["size"]), int(p["size"]))
        painter.end()

    def __del__(self):
        if hasattr(self, "_timer"):
            self._timer.stop()


class HolographicLogo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pulse_phase = 0.0
        self._scan_y = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)
        self.setFixedHeight(120)

    def _tick(self):
        self._pulse_phase += 0.05
        if self._pulse_phase > 2.0 * math.pi:
            self._pulse_phase -= 2.0 * math.pi
        self._scan_y += 2.0
        if self._scan_y > self.height():
            self._scan_y = 0.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        font = QFont("Segoe UI", 72, QFont.Bold)
        painter.setFont(font)

        text = "ACGTI"
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(text)
        tx = (self.width() - tw) / 2.0
        ty = (self.height() + fm.ascent() - fm.descent()) / 2.0

        pulse = 0.5 + 0.5 * math.sin(self._pulse_phase)
        glow_alpha = int(40 + 80 * pulse)

        for offset in range(4, 0, -1):
            glow_color = QColor(CYAN)
            glow_color.setAlpha(max(0, glow_alpha // offset))
            painter.setPen(QPen(glow_color, offset * 2.0))
            painter.drawText(int(tx), int(ty), text)

        r = int(pulse * 255)
        g = int(255 - pulse * 255)
        b = 255
        main_color = QColor(r, g, b, 240)
        painter.setPen(QPen(main_color, 1.0))
        painter.drawText(int(tx), int(ty), text)

        scan_gradient = QLinearGradient(0, self._scan_y - 8, 0, self._scan_y + 8)
        scan_gradient.setColorAt(0.0, QColor(0, 0, 0, 0))
        scan_gradient.setColorAt(0.5, QColor(255, 255, 255, 100))
        scan_gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(scan_gradient))
        painter.drawRect(int(tx), int(self._scan_y - 8), tw, 16)

        scanline_color = QColor(0, 0, 0, 20)
        painter.setPen(QPen(scanline_color, 1.0))
        for y in range(0, self.height(), 3):
            painter.drawLine(0, y, self.width(), y)

        painter.end()

    def __del__(self):
        if hasattr(self, "_timer"):
            self._timer.stop()


class EnergyBeamWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._x1 = 0.0
        self._y1 = 0.0
        self._x2 = 0.0
        self._y2 = 0.0
        self._progress = 0.0
        self._trail_particles = []
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def setEndpoints(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def _tick(self):
        self._progress += 0.02
        if self._progress > 1.0:
            self._progress = 0.0

        t = self._progress
        px = self._x1 + (self._x2 - self._x1) * t
        py = self._y1 + (self._y2 - self._y1) * t
        self._trail_particles.append({
            "x": px + random.uniform(-3, 3),
            "y": py + random.uniform(-3, 3),
            "life": 1.0,
            "size": random.uniform(1.5, 4.0),
        })

        alive = []
        for p in self._trail_particles:
            p["life"] -= 0.05
            p["y"] += random.uniform(-0.5, 0.5)
            p["x"] += random.uniform(-0.5, 0.5)
            if p["life"] > 0:
                alive.append(p)
        self._trail_particles = alive[-80:]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        dx = self._x2 - self._x1
        dy = self._y2 - self._y1
        length = math.sqrt(dx * dx + dy * dy)
        if length < 1:
            painter.end()
            return

        for p in self._trail_particles:
            alpha = int(p["life"] * 180)
            color = QColor(CYAN)
            color.setAlpha(alpha)
            gradient = QRadialGradient(p["x"], p["y"], p["size"] * 2)
            gradient.setColorAt(0.0, color)
            fade = QColor(CYAN)
            fade.setAlpha(0)
            gradient.setColorAt(1.0, fade)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(gradient))
            sz = p["size"] * 4
            painter.drawEllipse(int(p["x"] - sz / 2), int(p["y"] - sz / 2), int(sz), int(sz))

        for w, alpha_base in [(8, 25), (4, 50), (2, 120), (1, 255)]:
            beam_color = QColor(CYAN)
            beam_color.setAlpha(alpha_base)
            painter.setPen(QPen(beam_color, w))
            ex = self._x1 + dx * self._progress
            ey = self._y1 + dy * self._progress
            painter.drawLine(int(self._x1), int(self._y1), int(ex), int(ey))

        head_color = QColor(255, 255, 255, 200)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(head_color))
        hx = self._x1 + dx * self._progress
        hy = self._y1 + dy * self._progress
        painter.drawEllipse(int(hx - 3), int(hy - 3), 6, 6)

        glow = QColor(CYAN)
        glow.setAlpha(100)
        grad = QRadialGradient(hx, hy, 12)
        grad.setColorAt(0.0, glow)
        glow2 = QColor(CYAN)
        glow2.setAlpha(0)
        grad.setColorAt(1.0, glow2)
        painter.setBrush(QBrush(grad))
        painter.drawEllipse(int(hx - 12), int(hy - 12), 24, 24)

        painter.end()

    def __del__(self):
        if hasattr(self, "_timer"):
            self._timer.stop()


class DestinyCompass(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._e_pct = 50.0
        self._s_pct = 50.0
        self._t_pct = 50.0
        self._j_pct = 50.0
        self._target_e = 50.0
        self._target_s = 50.0
        self._target_t = 50.0
        self._target_j = 50.0
        self._angle_offset = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)
        self.setMinimumSize(250, 250)

    def setValues(self, e_pct, s_pct, t_pct, j_pct):
        self._target_e = max(0, min(100, e_pct))
        self._target_s = max(0, min(100, s_pct))
        self._target_t = max(0, min(100, t_pct))
        self._target_j = max(0, min(100, j_pct))

    def _tick(self):
        lerp = 0.08
        self._e_pct += (self._target_e - self._e_pct) * lerp
        self._s_pct += (self._target_s - self._s_pct) * lerp
        self._t_pct += (self._target_t - self._t_pct) * lerp
        self._j_pct += (self._target_j - self._j_pct) * lerp
        self._angle_offset += 0.5
        if self._angle_offset >= 360.0:
            self._angle_offset -= 360.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        cx = self.width() / 2.0
        cy = self.height() / 2.0
        radius = min(cx, cy) * 0.85

        self._draw_outer_ring(painter, cx, cy, radius)
        self._draw_inner_ring(painter, cx, cy, radius * 0.78)
        self._draw_dimension_lines(painter, cx, cy, radius)
        self._draw_pointers(painter, cx, cy, radius)
        self._draw_labels(painter, cx, cy, radius)
        self._draw_center(painter, cx, cy, radius * 0.15)

        painter.end()

    def _draw_outer_ring(self, painter, cx, cy, radius):
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self._angle_offset * 0.2)

        glow = QRadialGradient(0, 0, radius * 1.05)
        glow.setColorAt(0.85, QColor(0, 0, 0, 0))
        glow.setColorAt(0.95, QColor(CYAN + "30"))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(glow))
        r = int(radius * 1.05)
        painter.drawEllipse(-r, -r, 2 * r, 2 * r)

        ring_color = QColor(CYAN)
        ring_color.setAlpha(180)
        painter.setPen(QPen(ring_color, 2.0))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(int(-radius), int(-radius), int(2 * radius), int(2 * radius))

        inner = int(radius * 0.92)
        inner_color = QColor(BLUE)
        inner_color.setAlpha(100)
        painter.setPen(QPen(inner_color, 1.0))
        painter.drawEllipse(-inner, -inner, 2 * inner, 2 * inner)

        painter.setPen(QPen(ring_color, 1.0))
        from PySide6.QtGui import QPolygonF
        hex_poly = QPolygonF()
        for i in range(12):
            angle = (2.0 * math.pi * i) / 12.0
            hex_poly.append(QPointF(radius * 0.96 * math.cos(angle), radius * 0.96 * math.sin(angle)))
        painter.drawPolygon(hex_poly)

        tick_color = QColor(CYAN)
        tick_color.setAlpha(120)
        painter.setPen(QPen(tick_color, 1.0))
        for i in range(36):
            angle = (2.0 * math.pi * i) / 36.0
            x1 = radius * 0.92 * math.cos(angle)
            y1 = radius * 0.92 * math.sin(angle)
            x2 = radius * math.cos(angle)
            y2 = radius * math.sin(angle)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        font = QFont("Segoe UI Symbol", max(6, int(radius * 0.06)))
        painter.setFont(font)
        symbol_color = QColor(MAGENTA)
        symbol_color.setAlpha(150)
        painter.setPen(symbol_color)
        for i in range(12):
            angle = (2.0 * math.pi * i) / 12.0
            sx = radius * 0.88 * math.cos(angle)
            sy = radius * 0.88 * math.sin(angle)
            painter.drawText(int(sx) - 4, int(sy) + 4, RUNIC_SYMBOLS[i % len(RUNIC_SYMBOLS)])

        painter.restore()

    def _draw_inner_ring(self, painter, cx, cy, radius):
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(-self._angle_offset * 0.15)

        ring_color = QColor(PURPLE)
        ring_color.setAlpha(140)
        painter.setPen(QPen(ring_color, 1.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(int(-radius), int(-radius), int(2 * radius), int(2 * radius))

        fill_color = QColor(PURPLE)
        fill_color.setAlpha(8)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(fill_color))
        painter.drawEllipse(int(-radius), int(-radius), int(2 * radius), int(2 * radius))

        from PySide6.QtGui import QPolygonF
        painter.setPen(QPen(ring_color, 0.8))
        painter.setBrush(Qt.NoBrush)
        inner_hex = QPolygonF()
        for i in range(8):
            angle = (2.0 * math.pi * i) / 8.0
            inner_hex.append(QPointF(radius * 0.85 * math.cos(angle), radius * 0.85 * math.sin(angle)))
        painter.drawPolygon(inner_hex)

        painter.restore()

    def _draw_dimension_lines(self, painter, cx, cy, radius):
        dims = [
            (0.0, self._e_pct, "E", "I", CYAN),
            (90.0, self._s_pct, "S", "N", ORANGE),
            (180.0, self._t_pct, "T", "F", MAGENTA),
            (270.0, self._j_pct, "J", "P", PURPLE),
        ]
        painter.save()
        painter.translate(cx, cy)
        for base_angle, pct, pos_label, neg_label, color_str in dims:
            angle_rad = math.radians(base_angle)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            line_color = QColor(color_str)
            line_color.setAlpha(60)
            painter.setPen(QPen(line_color, 1.0, Qt.DotLine))
            inner_r = radius * 0.22
            outer_r = radius * 0.75
            painter.drawLine(
                int(inner_r * cos_a), int(inner_r * sin_a),
                int(outer_r * cos_a), int(outer_r * sin_a),
            )

            dot_r = radius * 0.75
            dot_x = dot_r * cos_a
            dot_y = dot_r * sin_a
            dot_color = QColor(color_str)
            dot_color.setAlpha(180)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(dot_color))
            painter.drawEllipse(int(dot_x - 3), int(dot_y - 3), 6, 6)

        painter.restore()

    def _draw_pointers(self, painter, cx, cy, radius):
        dims = [
            (0.0, self._e_pct, CYAN),
            (90.0, self._s_pct, ORANGE),
            (180.0, self._t_pct, MAGENTA),
            (270.0, self._j_pct, PURPLE),
        ]
        painter.save()
        painter.translate(cx, cy)

        for base_angle, pct, color_str in dims:
            angle_rad = math.radians(base_angle)
            offset = (pct / 100.0 - 0.5) * 2.0
            ptr_len = radius * 0.30 + abs(offset) * radius * 0.15

            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            tip_x = ptr_len * cos_a
            tip_y = ptr_len * sin_a

            perp_cos = math.cos(angle_rad + math.pi / 2.0)
            perp_sin = math.sin(angle_rad + math.pi / 2.0)
            base_w = 5.0
            base1_x = 12.0 * cos_a + base_w * perp_cos
            base1_y = 12.0 * sin_a + base_w * perp_sin
            base2_x = 12.0 * cos_a - base_w * perp_cos
            base2_y = 12.0 * sin_a - base_w * perp_sin

            pointer_color = QColor(color_str)
            pointer_color.setAlpha(200)
            painter.setPen(QPen(pointer_color, 1.0))
            painter.setBrush(Qt.NoBrush)

            from PySide6.QtGui import QPolygonF
            ptr = QPolygonF()
            ptr.append(QPointF(tip_x, tip_y))
            ptr.append(QPointF(base1_x, base1_y))
            ptr.append(QPointF(base2_x, base2_y))
            painter.drawPolygon(ptr)

            fill = QColor(color_str)
            fill.setAlpha(60)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(fill))
            painter.drawPolygon(ptr)

            glow_color = QColor(color_str)
            glow_color.setAlpha(int(40 + abs(offset) * 80))
            grad = QRadialGradient(tip_x, tip_y, 10)
            grad.setColorAt(0.0, glow_color)
            fade = QColor(color_str)
            fade.setAlpha(0)
            grad.setColorAt(1.0, fade)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(int(tip_x - 10), int(tip_y - 10), 20, 20)

        painter.restore()

    def _draw_labels(self, painter, cx, cy, radius):
        dims = [
            (0.0, "E / I", CYAN),
            (90.0, "S / N", ORANGE),
            (180.0, "T / F", MAGENTA),
            (270.0, "J / P", PURPLE),
        ]
        painter.save()
        painter.translate(cx, cy)

        font = QFont("Segoe UI", max(8, int(radius * 0.08)), QFont.Bold)
        painter.setFont(font)

        for base_angle, label, color_str in dims:
            angle_rad = math.radians(base_angle)
            label_r = radius * 0.65
            lx = label_r * math.cos(angle_rad)
            ly = label_r * math.sin(angle_rad)
            color = QColor(color_str)
            color.setAlpha(220)
            painter.setPen(QPen(color, 1.0))
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(label)
            painter.drawText(int(lx - tw / 2), int(ly + fm.ascent() / 2 - fm.descent() / 2), label)

        painter.restore()

    def _draw_center(self, painter, cx, cy, radius):
        glow = QRadialGradient(cx, cy, radius * 2)
        glow.setColorAt(0.0, QColor(255, 255, 255, 120))
        glow.setColorAt(0.4, QColor(CYAN + "40"))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(glow))
        r2 = int(radius * 2)
        painter.drawEllipse(int(cx - r2), int(cy - r2), 2 * r2, 2 * r2)

        ring_color = QColor(CYAN)
        ring_color.setAlpha(200)
        painter.setPen(QPen(ring_color, 1.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(int(cx - radius), int(cy - radius), int(2 * radius), int(2 * radius))

        core = QRadialGradient(cx, cy, radius)
        core.setColorAt(0.0, QColor(255, 255, 255, 180))
        core.setColorAt(0.5, QColor(CYAN + "80"))
        core.setColorAt(1.0, QColor(CYAN + "00"))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(core))
        painter.drawEllipse(int(cx - radius), int(cy - radius), int(2 * radius), int(2 * radius))

    def __del__(self):
        if hasattr(self, "_timer"):
            self._timer.stop()
