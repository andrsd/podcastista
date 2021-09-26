from PyQt5 import QtWidgets, QtCore


class EpisodePlayButton(QtWidgets.QPushButton):

    def __init__(self, icon_normal, icon_selected, parent=None):
        super().__init__(parent)
        self._icons = [icon_normal, icon_selected]
        self.setIcon(self._icons[0])
        self.setSize(QtCore.QSize(32, 32))
        self.setStyleSheet("""
            QPushButton {
                border: none;
            }
            """)
        self.setFlat(True)

    def setSize(self, size):
        self.setIconSize(size)
        self.setFixedSize(size)

    def enterEvent(self, event):
        self.setIcon(self._icons[1])

    def leaveEvent(self, event):
        self.setIcon(self._icons[0])
