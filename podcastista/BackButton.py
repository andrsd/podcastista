from PyQt5 import QtWidgets


class BackButton(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super().__init__("\u276C", parent)

        css = """
            QPushButton {
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444;
                border: none;
            }
            """
        self.setFlat(True)
        self.setStyleSheet(css)
        self.setFixedWidth(30)
        self.setFixedHeight(28)
        self.setContentsMargins(0, 0, 0, 0)
