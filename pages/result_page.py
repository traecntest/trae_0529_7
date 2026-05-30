import math
import random
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QRadialGradient, QLinearGradient, QPainterPath
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mbti_data import PERSONALITY_TYPES, ARCHETYPE_INFO
from widgets import ParticleWidget


class SilhouetteWidget(QWidget):
    def __init__(self, color_theme, archetype_class, parent=None):
        super().__init__(parent)
        self._color_theme = color_theme
        self._archetype_class = archetype_class
        self._pulse_phase = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)
        self.setMinimumSize(280, 380)

    def _tick(self):
        self._pulse_phase += 0.05
        if self._pulse_phase > 2.0 * math.pi:
            self._pulse_phase -= 2.0 * math.pi
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        cx = self.width() / 2.0
        cy = self.height() / 2.0

        base_color = QColor(self._color_theme)
        pulse = 0.5 + 0.5 * math.sin(self._pulse_phase)

        self._draw_glow(painter, cx, cy, base_color, pulse)
        self._draw_silhouette(painter, cx, cy, base_color)
        self._draw_archetype_symbol(painter, cx, cy, base_color)

        painter.end()

    def _draw_glow(self, painter, cx, cy, base_color, pulse):
        glow_layers = [
            (250, 0.15),
            (200, 0.25),
            (150, 0.35),
            (100, 0.45),
        ]

        for alpha, scale in glow_layers:
            glow_r = 120 * scale
            glow = QRadialGradient(cx, cy, glow_r)
            c = QColor(base_color)
            c.setAlpha(int(alpha * (0.5 + 0.5 * pulse)))
            glow.setColorAt(0.0, c)
            c2 = QColor(base_color)
            c2.setAlpha(0)
            glow.setColorAt(1.0, c2)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(glow))
            r = int(glow_r)
            painter.drawEllipse(int(cx - r), int(cy - r), 2 * r, 2 * r)

    def _draw_silhouette(self, painter, cx, cy, base_color):
        path = QPainterPath()

        head_r = 35
        head_y = cy - 80

        path.moveTo(cx, head_y - head_r)
        path.quadTo(cx + head_r, head_y - head_r, cx + head_r, head_y)
        path.quadTo(cx + head_r, head_y + head_r, cx, head_y + head_r)
        path.quadTo(cx - head_r, head_y + head_r, cx - head_r, head_y)
        path.quadTo(cx - head_r, head_y - head_r, cx, head_y - head_r)

        body_top_y = head_y + head_r
        body_width = 70
        body_height = 120

        path.moveTo(cx - body_width / 2, body_top_y)
        path.lineTo(cx - body_width / 2 - 20, body_top_y + body_height * 0.3)
        path.lineTo(cx - body_width / 2, body_top_y + body_height)
        path.lineTo(cx + body_width / 2, body_top_y + body_height)
        path.lineTo(cx + body_width / 2 + 20, body_top_y + body_height * 0.3)
        path.lineTo(cx + body_width / 2, body_top_y)

        arm_width = 25
        arm_length = 80
        arm_angle = 0.3

        path.moveTo(cx - body_width / 2, body_top_y + 20)
        path.lineTo(cx - body_width / 2 - arm_length * math.cos(arm_angle), body_top_y + 20 + arm_length * math.sin(arm_angle))
        path.lineTo(cx - body_width / 2 - arm_length * math.cos(arm_angle) + 15, body_top_y + 20 + arm_length * math.sin(arm_angle) + 30)
        path.lineTo(cx - body_width / 2 + 15, body_top_y + 50)

        path.moveTo(cx + body_width / 2, body_top_y + 20)
        path.lineTo(cx + body_width / 2 + arm_length * math.cos(arm_angle), body_top_y + 20 + arm_length * math.sin(arm_angle))
        path.lineTo(cx + body_width / 2 + arm_length * math.cos(arm_angle) - 15, body_top_y + 20 + arm_length * math.sin(arm_angle) + 30)
        path.lineTo(cx + body_width / 2 - 15, body_top_y + 50)

        leg_width = 30
        leg_height = 100

        path.moveTo(cx - 20, body_top_y + body_height)
        path.lineTo(cx - 35, body_top_y + body_height + leg_height)
        path.lineTo(cx - 10, body_top_y + body_height + leg_height)
        path.lineTo(cx, body_top_y + body_height + 20)
        path.lineTo(cx + 10, body_top_y + body_height + leg_height)
        path.lineTo(cx + 35, body_top_y + body_height + leg_height)
        path.lineTo(cx + 20, body_top_y + body_height)

        fill_color = QColor(base_color)
        fill_color.setAlpha(220)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(fill_color))
        painter.drawPath(path)

        outline_pen = QPen(QColor(255, 255, 255, 180), 2)
        painter.setPen(outline_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

    def _draw_archetype_symbol(self, painter, cx, cy, base_color):
        archetype_symbols = {
            "战士": "⚔",
            "魔术师": "✦",
            "守卫": "◆",
            "探索者": "◈",
            "统帅": "★",
            "游侠": "➤",
            "贤者": "☽",
            "吟游诗人": "♪",
        }
        symbol = archetype_symbols.get(self._archetype_class, "✧")

        font = QFont("Segoe UI Symbol", 32, QFont.Bold)
        painter.setFont(font)
        text_color = QColor(255, 255, 255, 220)
        painter.setPen(text_color)
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(symbol)
        painter.drawText(int(cx - tw / 2), int(cy - 40), symbol)

    def __del__(self):
        if hasattr(self, '_timer'):
            self._timer.stop()


class FloatingParticles(QWidget):
    def __init__(self, center_x, center_y, color_theme, parent=None):
        super().__init__(parent)
        self._center_x = center_x
        self._center_y = center_y
        self._color_theme = color_theme
        self._particles = []
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def _tick(self):
        if len(self._particles) < 20:
            self._particles.append(self._new_particle())
        for p in self._particles:
            p["life"] -= 0.02
            p["y"] -= p["speed"]
            p["x"] += p["drift"]
            p["angle"] += p["rot_speed"]
        self._particles = [p for p in self._particles if p["life"] > 0]
        self.update()

    def _new_particle(self):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(50, 150)
        return {
            "x": self._center_x + dist * math.cos(angle),
            "y": self._center_y + dist * math.sin(angle),
            "size": random.uniform(2, 5),
            "speed": random.uniform(0.5, 1.5),
            "drift": random.uniform(-0.5, 0.5),
            "life": 1.0,
            "angle": random.uniform(0, 360),
            "rot_speed": random.uniform(-2, 2),
        }

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        for p in self._particles:
            color = QColor(self._color_theme)
            color.setAlpha(int(p["life"] * 200))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(p["x"] - p["size"] / 2), int(p["y"] - p["size"] / 2), int(p["size"]), int(p["size"]))
        painter.end()

    def update_center(self, x, y):
        self._center_x = x
        self._center_y = y

    def __del__(self):
        if hasattr(self, '_timer'):
            self._timer.stop()


class TraitPanel(QFrame):
    def __init__(self, title, traits, color, parent=None):
        super().__init__(parent)
        self._color = color
        self.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(10, 10, 30, 200);
                border: 2px solid {color};
                border-radius: 15px;
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(color))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 18px;
                font-weight: bold;
                font-family: 'Consolas', 'Monaco', monospace;
            }}
        """)
        layout.addWidget(title_label)

        for trait in traits:
            trait_label = QLabel(f"> {trait}")
            trait_label.setStyleSheet(f"""
                QLabel {{
                    color: #E0E0E0;
                    font-size: 12px;
                    font-family: 'Consolas', 'Monaco', monospace;
                }}
            """)
            layout.addWidget(trait_label)

        layout.addStretch()


class AnimatedProgressBar(QWidget):
    def __init__(self, left_label, right_label, percentage, color, parent=None):
        super().__init__(parent)
        self._percentage = percentage
        self._target_percentage = percentage
        self._color = color
        self._animated_value = 0.0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        labels_layout = QHBoxLayout()
        self._left_label = QLabel(left_label)
        self._left_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")
        self._right_label = QLabel(right_label)
        self._right_label.setStyleSheet("color: #888888; font-size: 14px;")
        self._pct_label = QLabel(f"{int(percentage)}%")
        self._pct_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")
        labels_layout.addWidget(self._left_label)
        labels_layout.addStretch()
        labels_layout.addWidget(self._pct_label)
        labels_layout.addStretch()
        labels_layout.addWidget(self._right_label)
        layout.addLayout(labels_layout)

        self._bar_container = QWidget()
        self._bar_container.setFixedHeight(20)
        layout.addWidget(self._bar_container)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def set_target(self, value):
        self._target_percentage = value

    def _tick(self):
        diff = self._target_percentage - self._animated_value
        if abs(diff) > 0.1:
            self._animated_value += diff * 0.08
            self.update()
        self._pct_label.setText(f"{int(self._animated_value):.0f}%")
        self._bar_container.update()

    def paintEvent(self, event):
        painter = QPainter(self._bar_container)
        painter.setRenderHint(QPainter.Antialiasing, True)

        w = self._bar_container.width()
        h = self._bar_container.height()

        bg_color = QColor(30, 30, 50)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(0, 0, w, h, 10, 10)

        bar_width = int(w * self._animated_value / 100.0)

        if bar_width > 0:
            gradient = QLinearGradient(0, 0, bar_width, 0)
            c = QColor(self._color)
            gradient.setColorAt(0.0, c)
            c.setAlpha(150)
            gradient.setColorAt(1.0, c)
            painter.setBrush(QBrush(gradient))
            painter.drawRoundedRect(0, 0, bar_width, h, 10, 10)

            glow = QRadialGradient(bar_width - 10, h / 2, 20)
            glow_c = QColor(self._color)
            glow_c.setAlpha(100)
            glow.setColorAt(0.0, glow_c)
            glow.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(glow))
            painter.drawRoundedRect(max(0, bar_width - 40), 0, 40, h, 10, 10)

        painter.end()

    def __del__(self):
        if hasattr(self, '_timer'):
            self._timer.stop()


class ResultPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animations = []
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("""
            ResultPage {
                background-color: transparent;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        left_panel = self._create_left_panel()
        center_panel = self._create_center_panel()
        right_panel = self._create_right_panel()

        content_layout.addWidget(left_panel, 1)
        content_layout.addWidget(center_panel, 1)
        content_layout.addWidget(right_panel, 1)

        main_layout.addLayout(content_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._create_retest_button())
        buttons_layout.addSpacing(20)
        buttons_layout.addWidget(self._create_share_button())
        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)

    def _create_left_panel(self):
        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background-color: rgba(10, 10, 30, 150);
                border-radius: 20px;
                border: 1px solid rgba(0, 255, 255, 50);
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 255, 255, 50))
        shadow.setOffset(0, 0)
        panel.setGraphicsEffect(shadow)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        self._type_name = QLabel()
        self._type_name.setStyleSheet("""
            QLabel {
                color: #00FFFF;
                font-size: 32px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self._type_name)

        self._type_subtitle = QLabel()
        self._type_subtitle.setStyleSheet("""
            QLabel {
                color: #FF00FF;
                font-size: 16px;
                font-style: italic;
            }
        """)
        layout.addWidget(self._type_subtitle)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 30);")
        layout.addWidget(separator)

        self._type_description = QLabel()
        self._type_description.setWordWrap(True)
        self._type_description.setStyleSheet("""
            QLabel {
                color: #CCCCCC;
                font-size: 13px;
                line-height: 1.6;
            }
        """)
        layout.addWidget(self._type_description)

        layout.addStretch()

        self._dimensions_layout = QVBoxLayout()
        layout.addLayout(self._dimensions_layout)

        return panel

    def _create_center_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        self._silhouette_container = QWidget()
        self._silhouette_layout = QVBoxLayout(self._silhouette_container)
        self._silhouette_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._silhouette_container, 1)

        archetype_layout = QHBoxLayout()
        archetype_layout.setSpacing(30)

        self._emblem_label = QLabel()
        self._emblem_label.setStyleSheet("""
            QLabel {
                color: #FFD700;
                font-size: 48px;
            }
        """)
        archetype_layout.addWidget(self._emblem_label)

        archetype_info_layout = QVBoxLayout()
        self._class_label = QLabel()
        self._class_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        archetype_info_layout.addWidget(self._class_label)

        self._weapon_label = QLabel()
        self._weapon_label.setStyleSheet("""
            QLabel {
                color: #AAAAAA;
                font-size: 14px;
            }
        """)
        archetype_info_layout.addWidget(self._weapon_label)

        self._armor_label = QLabel()
        self._armor_label.setStyleSheet("""
            QLabel {
                color: #AAAAAA;
                font-size: 14px;
            }
        """)
        archetype_info_layout.addWidget(self._armor_label)

        archetype_layout.addLayout(archetype_info_layout)
        archetype_layout.addStretch()

        layout.addLayout(archetype_layout)

        return panel

    def _create_right_panel(self):
        panel = QWidget()
        self._right_layout = QVBoxLayout(panel)
        self._right_layout.setContentsMargins(0, 0, 0, 0)
        self._right_layout.setSpacing(20)

        self._strengths_panel = TraitPanel("/// 优势", [], "#00FFFF")
        self._right_layout.addWidget(self._strengths_panel, 1)

        self._weaknesses_panel = TraitPanel("/// 劣势", [], "#FF6B6B")
        self._right_layout.addWidget(self._weaknesses_panel, 1)

        return panel

    def _create_retest_button(self):
        btn = QPushButton("重新测试")
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #00FFFF;
                color: #00FFFF;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 40px;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 255, 30);
                border-color: #FF00FF;
                color: #FF00FF;
            }
        """)
        btn.clicked.connect(self._on_retest)
        return btn

    def _create_share_button(self):
        btn = QPushButton("分享结果")
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #FF00FF;
                color: #FF00FF;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 40px;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 255, 30);
                border-color: #00FFFF;
                color: #00FFFF;
            }
        """)
        btn.clicked.connect(self._on_share)
        return btn

    def showEvent(self, event):
        super().showEvent(event)
        self._load_result()
        QTimer.singleShot(100, self._start_animations)

    def _load_result(self):
        parent_window = self.window()
        result_type = parent_window.get_result_type()
        type_data = PERSONALITY_TYPES.get(result_type, {})

        self._type_name.setText(type_data.get("name", "未知类型"))
        self._type_subtitle.setText(type_data.get("subtitle", ""))
        self._type_description.setText(type_data.get("description", ""))

        color_theme = type_data.get("color_theme", "#00FFFF")
        archetype_class = type_data.get("archetype_class", "")

        for i in reversed(range(self._silhouette_layout.count())):
            item = self._silhouette_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        self._silhouette = SilhouetteWidget(color_theme, archetype_class)
        self._silhouette_layout.addWidget(self._silhouette, 0, Qt.AlignCenter)

        archetype_info = ARCHETYPE_INFO.get(archetype_class, {})
        self._emblem_label.setText(archetype_info.get("emblem", "✧"))
        self._class_label.setText(f"职业: {archetype_class}")
        self._weapon_label.setText(f"武器: {archetype_info.get('weapon', '')}")
        self._armor_label.setText(f"护甲: {archetype_info.get('armor', '')}")

        for i in reversed(range(self._right_layout.count())):
            item = self._right_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        self._strengths_panel = TraitPanel("/// 优势", type_data.get("strengths", []), "#00FFFF")
        self._weaknesses_panel = TraitPanel("/// 劣势", type_data.get("weaknesses", []), "#FF6B6B")
        self._right_layout.addWidget(self._strengths_panel, 1)
        self._right_layout.addWidget(self._weaknesses_panel, 1)

        e_pct, s_pct, t_pct, j_pct = parent_window.get_percentages()
        self._update_dimension_bars(e_pct, s_pct, t_pct, j_pct)

    def _update_dimension_bars(self, e_pct, s_pct, t_pct, j_pct):
        for i in reversed(range(self._dimensions_layout.count())):
            item = self._dimensions_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        dimensions = [
            ("E", "I", e_pct, "#00FFFF"),
            ("S", "N", s_pct, "#FF8800"),
            ("T", "F", t_pct, "#FF00FF"),
            ("J", "P", j_pct, "#8800FF"),
        ]

        for left, right, pct, color in dimensions:
            bar = AnimatedProgressBar(left, right, pct, color)
            bar.set_target(pct)
            self._dimensions_layout.addWidget(bar)

    def _start_animations(self):
        widgets = [
            self._type_name, self._type_subtitle, self._type_description,
            self._silhouette, self._strengths_panel, self._weaknesses_panel
        ]

        for i, widget in enumerate(widgets):
            anim = QPropertyAnimation(widget, b"windowOpacity")
            anim.setDuration(500)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim.setStartDelay(i * 150)
            anim.start()
            self._animations.append(anim)

    def _on_retest(self):
        parent_window = self.window()
        parent_window.reset_test()
        parent_window.navigate_to_page_with_animation(0)

    def _on_share(self):
        QMessageBox.information(self, "分享", "分享功能开发中...")
