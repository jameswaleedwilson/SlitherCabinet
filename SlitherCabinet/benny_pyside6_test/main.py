# Operating system
import sys
# Python packages
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
# Local modules
from SlitherCabinet.benny_pyside6_test.animated_splash_screen import AnimatedSplashScreen
from SlitherCabinet.benny_pyside6_test.main_window import MainWindow


class OpenGLWindow(MainWindow):
    def __init__(self):
        super().__init__()


# 1.Close AnimatedSplashScreen() and open MainWindow()
def execute_functions():
    animated_splash_screen.finish(main_window)
    main_window.window.show()

# Run main program
if __name__ == "__main__":
    app = QApplication([])

    # Initialise AnimatedSplashScreen()
    animated_splash_screen = AnimatedSplashScreen()
    animated_splash_screen.show()
    # Allows the splash screen to be displayed immediately
    app.processEvents()

    # Initialise MainWindow()
    main_window = OpenGLWindow()

    # 2.Close AnimatedSplashScreen() and open MainWindow()
    timer = QTimer()
    timer.timeout.connect(execute_functions)
    timer.start(11600)

    sys.exit(app.exec())

