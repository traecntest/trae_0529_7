from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QColor, QFont, QPalette, QPainter, QLinearGradient

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from widgets import DestinyCompass, ParticleWidget, EnergyBeamWidget
from mbti_data import QUESTIONS


class TestPage(QWidget):
    answer_selected = Signal()

    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.current_index = 0
        self._hue_progress = 0.0

        self._setup_ui()
        self._update_question()

    def _setup_ui(self):
        self.setAutoFillBackground(True)
        self._update_background_color()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.particles = ParticleWidget(self)
        self.particles.lower()

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(40)

        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: transparent;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)

        self.compass = DestinyCompass()
        self.compass.setFixedSize(350, 350)
        left_layout.addWidget(self.compass)

        content_layout.addWidget(left_panel, 1)

        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: transparent;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(20)

        top_bar = QHBoxLayout()
        top_bar.setSpacing(20)

        self.back_btn = QPushButton("返回")
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.clicked.connect(self._go_back)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #8800FF;
                color: #8800FF;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: rgba(136, 0, 255, 30);
            }
        """)
        top_bar.addWidget(self.back_btn)
        top_bar.addStretch()

        self.question_num_label = QLabel()
        self.question_num_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.question_num_label.setStyleSheet("""
            QLabel {
                color: #00FFFF;
                font-size: 18px;
                font-weight: bold;
                font-family: "Segoe UI", sans-serif;
            }
        """)
        top_bar.addWidget(self.question_num_label)

        right_layout.addLayout(top_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 20);
                border: none;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00FFFF, stop:0.5 #FF00FF, stop:1 #FF8800);
                border-radius: 6px;
            }
        """)
        progress_shadow = QGraphicsDropShadowEffect()
        progress_shadow.setBlurRadius(20)
        progress_shadow.setColor(QColor(0, 255, 255, 150))
        progress_shadow.setOffset(0, 0)
        self.progress_bar.setGraphicsEffect(progress_shadow)
        right_layout.addWidget(self.progress_bar)

        right_layout.addSpacing(20)

        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 26px;
                font-weight: bold;
                font-family: "Segoe UI", sans-serif;
                padding: 30px 20px;
            }
        """)
        right_layout.addWidget(self.question_label)

        right_layout.addStretch()

        self.option_a = QPushButton()
        self.option_a.setCursor(Qt.PointingHandCursor)
        self.option_a.setMinimumHeight(80)
        self.option_a.clicked.connect(lambda: self._select_option('A'))
        self.option_a.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 10);
                border: 3px solid #00FFFF;
                color: #00FFFF;
                font-size: 18px;
                font-weight: bold;
                font-family: "Segoe UI", sans-serif;
                padding: 15px 30px;
                border-radius: 15px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 255, 30);
            }
            QPushButton:pressed {
                background-color: rgba(0, 255, 255, 50);
            }
        """)
        shadow_a = QGraphicsDropShadowEffect()
        shadow_a.setBlurRadius(30)
        shadow_a.setColor(QColor(0, 255, 255, 100))
        shadow_a.setOffset(0, 0)
        self.option_a.setGraphicsEffect(shadow_a)
        right_layout.addWidget(self.option_a)

        right_layout.addSpacing(15)

        self.option_b = QPushButton()
        self.option_b.setCursor(Qt.PointingHandCursor)
        self.option_b.setMinimumHeight(80)
        self.option_b.clicked.connect(lambda: self._select_option('B'))
        self.option_b.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 255, 10);
                border: 3px solid #FF00FF;
                color: #FF00FF;
                font-size: 18px;
                font-weight: bold;
                font-family: "Segoe UI", sans-serif;
                padding: 15px 30px;
                border-radius: 15px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 255, 30);
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 255, 50);
            }
        """)
        shadow_b = QGraphicsDropShadowEffect()
        shadow_b.setBlurRadius(30)
        shadow_b.setColor(QColor(255, 0, 255, 100))
        shadow_b.setOffset(0, 0)
        self.option_b.setGraphicsEffect(shadow_b)
        right_layout.addWidget(self.option_b)

        content_layout.addWidget(right_panel, 2)

        main_layout.addLayout(content_layout)

        self.energy_beam = EnergyBeamWidget(self)
        self.energy_beam.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.energy_beam.lower()

        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self._update_hue)
        self.color_timer.start(50)

        QTimer.singleShot(100, self._raise_interactive_widgets)

    def _raise_interactive_widgets(self):
        self.option_a.raise_()
        self.option_b.raise_()
        self.back_btn.raise_()

    def _update_background_color(self):
        palette = self.palette()
        r1, g1, b1 = 5, 5, 25
        r2, g2, b2 = 50, 30, 10
        t = self._hue_progress
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        palette.setColor(QPalette.Window, QColor(r, g, b))
        self.setPalette(palette)

    def _update_hue(self):
        target = self.current_index / max(1, len(QUESTIONS) - 1)
        self._hue_progress += (target - self._hue_progress) * 0.05
        self._update_background_color()

    def _update_question(self):
        if self.current_index >= len(QUESTIONS):
            self.parent_window.navigate_to_page_with_animation(2)
            return

        question = QUESTIONS[self.current_index]

        self.question_num_label.setText(f"第 {self.current_index + 1} / {len(QUESTIONS)} 题")
        progress = ((self.current_index) / len(QUESTIONS)) * 100
        self.progress_bar.setValue(int(progress))

        self.question_label.setText(question["text"])
        self.option_a.setText(f"A. {question['option_a']['text']}")
        self.option_b.setText(f"B. {question['option_b']['text']}")

        self.option_a.setEnabled(True)
        self.option_b.setEnabled(True)

    def _select_option(self, option):
        self.option_a.setEnabled(False)
        self.option_b.setEnabled(False)

        question = QUESTIONS[self.current_index]
        dimension = question["dimension"]

        if option == 'A':
            score = question["option_a"]["score"]
            self._flash_button(self.option_a, "#00FFFF")
        else:
            score = question["option_b"]["score"]
            self._flash_button(self.option_b, "#FF00FF")

        self.parent_window.record_answer(dimension, score)
        e_pct, s_pct, t_pct, j_pct = self.parent_window.get_percentages()
        self.compass.setValues(e_pct, s_pct, t_pct, j_pct)

        btn = self.option_a if option == 'A' else self.option_b
        self._trigger_energy_beam(btn)

        QTimer.singleShot(600, self._next_question)

    def _flash_button(self, button, color_hex):
        original_style = button.styleSheet()
        flash_style = f"""
            QPushButton {{
                background-color: {color_hex};
                border: 3px solid #FFFFFF;
                color: #000000;
                font-size: 18px;
                font-weight: bold;
                font-family: "Segoe UI", sans-serif;
                padding: 15px 30px;
                border-radius: 15px;
                text-align: left;
            }}
        """
        button.setStyleSheet(flash_style)
        QTimer.singleShot(150, lambda: button.setStyleSheet(original_style))

    def _trigger_energy_beam(self, button):
        btn_rect = button.geometry()
        parent_rect = self.geometry()

        x1 = btn_rect.center().x()
        y1 = btn_rect.center().y()

        compass_center_x = self.compass.geometry().center().x()
        compass_center_y = self.compass.geometry().center().y()

        self.energy_beam.setEndpoints(x1, y1, compass_center_x, compass_center_y)
        self.energy_beam.raise_()
        self.energy_beam.show()

        QTimer.singleShot(500, self._on_beam_finished)

    def _on_beam_finished(self):
        self.energy_beam.hide()
        self.energy_beam.lower()
        self._raise_interactive_widgets()

    def _next_question(self):
        self.current_index += 1
        self.parent_window.current_question = self.current_index
        self._update_question()

    def _go_back(self):
        self.parent_window.reset_test()
        self.parent_window.navigate_to_page_with_animation(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.particles.setGeometry(0, 0, self.width(), self.height())
        self.energy_beam.setGeometry(0, 0, self.width(), self.height())
        self.particles.lower()
        self.energy_beam.lower()
        self._raise_interactive_widgets()

    def reset(self):
        self.current_index = 0
        self._hue_progress = 0.0
        self.compass.setValues(50, 50, 50, 50)
        self._update_question()
        self._update_background_color()
