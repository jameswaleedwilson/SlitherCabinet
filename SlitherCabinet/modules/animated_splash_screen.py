# Operating system
""" none"""
# Python packages
from PyQt5.QtCore import QTimer, QDir
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QSplashScreen

# Local modules
""" none """


class AnimatedSplashScreen(QSplashScreen):
    def __init__(self):

        self.dir = QDir("frames")
        self.dir.setFilter(QDir.Files | QDir.NoDotAndDotDot)  # Filter to get only files, excluding "." and ".."
        self.file_names = self.dir.entryList()

        self.pixmap = []
        for i in range(len(self.file_names)):
            path = "frames/" + self.file_names[i]
            self.pixmap.append(QPixmap(path))

        super().__init__(self.pixmap[0])

        self.setWindowTitle("Slither")
        self.setWindowIcon(QIcon("icons/window.png"))
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setEnabled(False)

        self.duration = 42
        self.current_frame = 0
        self.run = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(self.duration)

    def update_frame(self):
        if self.current_frame == len(self.pixmap) - 1:
            self.run = False
        if self.run:
            self.current_frame = (self.current_frame + 1) % len(self.pixmap)
            self.setPixmap(self.pixmap[self.current_frame])
