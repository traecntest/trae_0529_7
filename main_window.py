import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPalette


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        from PySide6.QtGui import QPainter, QLinearGradient
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(5, 5, 25))
        gradient.setColorAt(0.5, QColor(10, 10, 40))
        gradient.setColorAt(1.0, QColor(5, 5, 25))
        
        painter.fillRect(self.rect(), gradient)
        painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ACGTI - 二次元人格测试")
        self.resize(1000, 700)
        
        self._setup_style()
        self._setup_central_widget()
        
        self.scores = {
            "E": 0, "I": 0,
            "S": 0, "N": 0,
            "T": 0, "F": 0,
            "J": 0, "P": 0
        }
        self.current_question = 0
        
        from widgets import MagicCircleWidget, ParticleWidget
        
        self.magic_circle = MagicCircleWidget(self)
        self.particles = ParticleWidget(self)
        
        self.background = BackgroundWidget(self)
        self.background.lower()
        
    def _setup_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #050519;
            }
            QPushButton {
                background-color: transparent;
                border: 2px solid #00FFFF;
                color: #00FFFF;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 30px;
                border-radius: 25px;
                outline: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 255, 30);
                border-color: #FF00FF;
                color: #FF00FF;
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 255, 50);
            }
            QLabel {
                color: #FFFFFF;
                font-family: "Segoe UI", sans-serif;
            }
        """)
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(5, 5, 25))
        self.setPalette(palette)

    def _setup_central_widget(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'magic_circle'):
            self.magic_circle.setGeometry(0, 0, self.width(), self.height())
            self.particles.setGeometry(0, 0, self.width(), self.height())
            self.background.setGeometry(0, 0, self.width(), self.height())
            
    def add_page(self, page):
        self.stacked_widget.addWidget(page)
        
    def navigate_to_page(self, page_index):
        self.stacked_widget.setCurrentIndex(page_index)
        
    def navigate_to_page_with_animation(self, page_index):
        current_widget = self.stacked_widget.currentWidget()
        
        self.animation = QPropertyAnimation(current_widget, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(lambda: self._finish_navigation(page_index))
        self.animation.start()
        
    def _finish_navigation(self, page_index):
        self.stacked_widget.setCurrentIndex(page_index)
        new_widget = self.stacked_widget.currentWidget()
        new_widget.setWindowOpacity(0.0)
        
        self.animation2 = QPropertyAnimation(new_widget, b"windowOpacity")
        self.animation2.setDuration(300)
        self.animation2.setStartValue(0.0)
        self.animation2.setEndValue(1.0)
        self.animation2.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation2.start()
        
    def record_answer(self, dimension, option):
        self.scores[option] += 1
        
    def get_result_type(self):
        result = ""
        result += "E" if self.scores["E"] >= self.scores["I"] else "I"
        result += "S" if self.scores["S"] >= self.scores["N"] else "N"
        result += "T" if self.scores["T"] >= self.scores["F"] else "F"
        result += "J" if self.scores["J"] >= self.scores["P"] else "P"
        return result
        
    def get_percentages(self):
        e_pct = (self.scores["E"] / max(1, self.scores["E"] + self.scores["I"])) * 100
        s_pct = (self.scores["S"] / max(1, self.scores["S"] + self.scores["N"])) * 100
        t_pct = (self.scores["T"] / max(1, self.scores["T"] + self.scores["F"])) * 100
        j_pct = (self.scores["J"] / max(1, self.scores["J"] + self.scores["P"])) * 100
        return e_pct, s_pct, t_pct, j_pct
        
    def reset_test(self):
        self.scores = {
            "E": 0, "I": 0,
            "S": 0, "N": 0,
            "T": 0, "F": 0,
            "J": 0, "P": 0
        }
        self.current_question = 0
