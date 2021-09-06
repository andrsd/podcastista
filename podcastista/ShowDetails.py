from PyQt5 import QtWidgets


class ShowDetails(QtWidgets.QWidget):
    """
    Widget on main window with show details
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self.setupWidgets()
        self.fill()

    def setupWidgets(self):
        layout = QtWidgets.QVBoxLayout(self)

        self._back = QtWidgets.QPushButton("Back")
        self._back.clicked.connect(self.onBack)
        layout.addWidget(self._back)

        self._show_artwork = QtWidgets.QLabel("Artwork")
        layout.addWidget(self._show_artwork)

        self._show_title = QtWidgets.QLabel("Title")
        layout.addWidget(self._show_title)

        self._show_author = QtWidgets.QLabel("Author")
        layout.addWidget(self._show_author)

        self._show_description = QtWidgets.QLabel("Show description")
        layout.addWidget(self._show_description)

        self._episodes_label = QtWidgets.QLabel("Episodes")
        layout.addWidget(self._episodes_label)

        self._episodes = QtWidgets.QListWidget()
        layout.addWidget(self._episodes)

        self.setLayout(layout)

    def fill(self):
        self._episodes.addItem("Episode 1")
        self._episodes.addItem("Episode 2")

    def onBack(self, item):
        self._main_window.viewMain()
