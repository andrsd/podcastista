from PyQt5 import QtWidgets


class InfoLabel(QtWidgets.QWidget):

    def __init__(self, title, text=None, parent=None):
        super().__init__(parent)

        font = self.font()
        font.setPointSizeF(font.pointSize() * 1.15)

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self._title = QtWidgets.QLabel(title)
        self._title.setFont(font)
        self._title.setStyleSheet("""
            color: #888
            """)
        self._title.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        self._layout.addWidget(self._title)

        self._text = QtWidgets.QLabel(text)
        self._text.setFont(font)
        self._text.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        self._layout.addWidget(self._text)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)

    def set(self, text):
        self._text.setText(text)
