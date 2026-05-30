import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from pages import WelcomePage, TestPage, ResultPage


def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    welcome_page = WelcomePage(window)
    test_page = TestPage(window)
    result_page = ResultPage(window)
    
    window.add_page(welcome_page)
    window.add_page(test_page)
    window.add_page(result_page)
    
    window.navigate_to_page(0)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
