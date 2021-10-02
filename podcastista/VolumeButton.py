from PyQt5 import QtWidgets, QtCore
from podcastista.assets import Assets


class VolumeButton(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlat(True)
        self.setCheckable(True)
        self.setSize(QtCore.QSize(20, 20))
        self.setIcon(Assets().volume_on_icon)
        self.setStyleSheet("""
            QPushButton {
                border: none;
            }
            """)
        self.clicked.connect(self.onClicked)

    def setSize(self, size):
        self.setIconSize(size)
        self.setFixedSize(size)

    def updateIcon(self):
        if self.isChecked():
            self.setIcon(Assets().volume_muted_icon)
        else:
            self.setIcon(Assets().volume_on_icon)

    def onClicked(self):
        self.updateIcon()
