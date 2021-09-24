from PyQt5 import QtWidgets, QtCore
from podcastista.assets import Assets


class EpisodePlayButton(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(Assets().ep_play_normal_icon)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setFixedSize(QtCore.QSize(32, 32))
        self.setStyleSheet("""
            QPushButton {
                border: none;
            }
            """)
        self.setFlat(True)

    def enterEvent(self, event):
        self.setIcon(Assets().ep_play_selected_icon)

    def leaveEvent(self, event):
        self.setIcon(Assets().ep_play_normal_icon)
