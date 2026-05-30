import math
import random

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QRadialGradient, QLinearGradient, QPainterPath
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QDialog, QDialogButtonBox, QGraphicsDropShadowEffect
)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from widgets import HolographicLogo, MagicCircleWidget, ParticleWidget, RUNIC_SYMBOLS, CYAN, MAGENTA, BLUE, PURPLE


class FloatingRuneWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._runes = []
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(50)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._init_runes()

    def _init_runes(self):
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(80, 180)
            self._runes.append({
                "symbol": random.choice(RUNIC_SYMBOLS),
                "angle": angle,
                "distance": dist,
                "speed": random.uniform(0.003, 0.008),
                "phase": random.uniform(0, 2 * math.pi),
                "size": random.uniform(14, 22),
                "color": random.choice([CYAN, MAGENTA, BLUE]),
            })

    def _tick(self):
        for r in self._runes:
            r["angle"] += r["speed"]
            r["phase"] += 0.05
            if r["angle"] > 2 * math.pi:
                r["angle"] -= 2 * math.pi
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        cx = self.width() / 2.0
        cy = self.height() / 2.0

        for r in self._runes:
            float_offset = math.sin(r["phase"]) * 8
            x = cx + (r["distance"] + float_offset) * math.cos(r["angle"])
            y = cy + (r["distance"] + float_offset) * math.sin(r["angle"])

            alpha = int(100 + 80 * math.sin(r["phase"]))
            color = QColor(r["color"])
            color.setAlpha(alpha)

            font = QFont("Segoe UI Symbol", int(r["size"]))
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(color)

            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(r["symbol"])
            th = fm.height()
            painter.drawText(int(x - tw / 2), int(y + th / 4), r["symbol"])

        painter.end()

    def __del__(self):
        if hasattr(self, "_timer"):
            self._timer.stop()


class GlowingLabel(QLabel):
    def __init__(self, text, color=CYAN, font_size=24, parent=None):
        super().__init__(text, parent)
        self._color = color
        self._font_size = font_size
        self._pulse_phase = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(50)
        self.setAlignment(Qt.AlignCenter)
        self._update_style()

    def _tick(self):
        self._pulse_phase += 0.08
        if self._pulse_phase > 2 * math.pi:
            self._pulse_phase -= 2 * math.pi
        self._update_style()

    def _update_style(self):
        pulse = 0.6 + 0.4 * math.sin(self._pulse_phase)
        glow_radius = int(10 + 5 * pulse)
        color = QColor(self._color)
        color.setAlpha(int(200 + 55 * pulse))
        self.setStyleSheet(f"""
            QLabel {{
                color: {color.name()};
                font-size: {self._font_size}px;
                font-weight: bold;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            }}
        """)
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(glow_radius)
        effect.setColor(QColor(self._color))
        effect.setOffset(0, 0)
        self.setGraphicsEffect(effect)

    def __del__(self):
        if hasattr(self, "_timer"):
            self._timer.stop()


class NeonButton(QPushButton):
    def __init__(self, text, color=CYAN, parent=None):
        super().__init__(text, parent)
        self._base_color = color
        self._hover = False
        self.setMinimumHeight(60)
        self.setMinimumWidth(220)
        self.setCursor(Qt.PointingHandCursor)
        self._update_style(False)

    def enterEvent(self, event):
        self._hover = True
        self._update_style(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self._update_style(False)
        super().leaveEvent(event)

    def _update_style(self, hover):
        if hover:
            bg_alpha = 40
            glow_radius = 25
        else:
            bg_alpha = 15
            glow_radius = 15
        color = QColor(self._base_color)
        bg_color = QColor(self._base_color)
        bg_color.setAlpha(bg_alpha)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({bg_color.red()}, {bg_color.green()}, {bg_color.blue()}, {bg_alpha / 255.0});
                color: {color.name()};
                border: 2px solid {color.name()};
                border-radius: 12px;
                font-size: 22px;
                font-weight: bold;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
                padding: 10px 30px;
            }}
            QPushButton:hover {{
                background-color: rgba({bg_color.red()}, {bg_color.green()}, {bg_color.blue()}, 0.25);
            }}
            QPushButton:pressed {{
                background-color: rgba({bg_color.red()}, {bg_color.green()}, {bg_color.blue()}, 0.4);
            }}
        """)
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(glow_radius)
        effect.setColor(QColor(self._base_color))
        effect.setOffset(0, 0)
        self.setGraphicsEffect(effect)


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于")
        self.setFixedSize(420, 380)
        self.setStyleSheet("""
            QDialog {
                background-color: #050519;
                border: 2px solid #00FFFF;
            }
        """)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(15)

        title = GlowingLabel("ACGTI MBTI", CYAN, 28)
        layout.addWidget(title)

        version = QLabel("版本: 1.0.0")
        version.setStyleSheet("""
            QLabel {
                color: #00FFFF;
                font-size: 16px;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            }
        """)
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        desc = QLabel("二次元幻想人格测试\n\n融合心理学与ACG幻想的MBTI测试\n探索你的二次元人格属性")
        desc.setStyleSheet("""
            QLabel {
                color: #AAAAFF;
                font-size: 14px;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            }
        """)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        credits_label = QLabel("制作人员")
        credits_label.setStyleSheet("""
            QLabel {
                color: #FF00FF;
                font-size: 16px;
                font-weight: bold;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            }
        """)
        credits_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(credits_label)

        credits = QLabel("ACGTI 开发团队\n\n感谢使用本应用")
        credits.setStyleSheet("""
            QLabel {
                color: #88AAFF;
                font-size: 13px;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            }
        """)
        credits.setAlignment(Qt.AlignCenter)
        credits.setWordWrap(True)
        layout.addWidget(credits)

        layout.addStretch()

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok)
        btn_box.setStyleSheet("""
            QDialogButtonBox QPushButton {
                background-color: rgba(0, 255, 255, 0.15);
                color: #00FFFF;
                border: 2px solid #00FFFF;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
                padding: 8px 20px;
                min-width: 100px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: rgba(0, 255, 255, 0.3);
            }
        """)
        btn_box.accepted.connect(self.accept)
        layout.addWidget(btn_box)

        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(30)
        effect.setColor(QColor(CYAN))
        effect.setOffset(0, 0)
        self.setGraphicsEffect(effect)


class WelcomePage(QWidget):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self._parent_window = parent_window
        self.setStyleSheet("background-color: #050519;")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._magic_circle = MagicCircleWidget(self)
        self._particles = ParticleWidget(self)
        self._floating_runes = FloatingRuneWidget(self)

        content_widget = QWidget(self)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(60, 40, 60, 40)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignCenter)

        logo_widget = QWidget()
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(10)
        logo_layout.setAlignment(Qt.AlignCenter)

        self._logo = HolographicLogo()
        self._logo.setFixedWidth(400)
        logo_layout.addWidget(self._logo)

        subtitle = GlowingLabel("二次元幻想人格测试", MAGENTA, 28)
        logo_layout.addWidget(subtitle)

        content_layout.addWidget(logo_widget)
        content_layout.addSpacing(30)

        description = QLabel("心理学与ACG幻想的完美融合\n探索属于你的二次元人格世界")
        description.setStyleSheet("""
            QLabel {
                color: #88CCFF;
                font-size: 18px;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            }
        """)
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        content_layout.addWidget(description)

        content_layout.addSpacing(40)

        start_btn = NeonButton("开始测试", CYAN)
        start_btn.clicked.connect(self._on_start_test)
        content_layout.addWidget(start_btn, 0, Qt.AlignCenter)

        content_layout.addSpacing(20)

        about_btn = NeonButton("关于", PURPLE)
        about_btn.setMinimumHeight(45)
        about_btn.setMinimumWidth(140)
        about_btn.clicked.connect(self._on_about)
        content_layout.addWidget(about_btn, 0, Qt.AlignCenter)

        content_layout.addStretch()

        main_layout.addWidget(content_widget)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._magic_circle.resize(self.size())
        self._particles.resize(self.size())
        self._floating_runes.resize(self.size())
        return super().resizeEvent(event)

    def _on_start_test(self):
        if self._parent_window:
            self._parent_window.navigate_to_page_with_animation(1)

    def _on_about(self):
        dialog = AboutDialog(self)
        dialog.exec()
