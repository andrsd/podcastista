from PyQt5 import QtWidgets


class SubsectionTitle(QtWidgets.QLabel):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        font = self.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 1.5)
        self.setFont(font)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
