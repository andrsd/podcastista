from PyQt5 import QtWidgets


class HLine(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setStyleSheet('color: #444')
