from PyQt5 import QtWidgets


class HLine(QtWidgets.QFrame):

    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setStyleSheet('color: #444')
