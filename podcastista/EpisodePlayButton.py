from PyQt5 import QtWidgets, QtCore
from podcastista.assets import Assets


class EpisodePlayButton(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(Assets().ep_play_normal_icon)
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
        self.setIcon(Assets().ep_play_selected_icon)

    def leaveEvent(self, event):
        self.setIcon(Assets().ep_play_normal_icon)
