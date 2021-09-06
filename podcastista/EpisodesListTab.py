from PyQt5 import QtWidgets


class EpisodesListTab(QtWidgets.QWidget):
    """
    Tab on the main window with the list of episodes
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self.setupWidgets()
        self.fill()

    def setupWidgets(self):
        layout = QtWidgets.QVBoxLayout(self)

        self._title = QtWidgets.QLabel("Episodes")
        layout.addWidget(self._title)

        self._episodes = QtWidgets.QListWidget()
        layout.addWidget(self._episodes)

        self.setLayout(layout)

    def fill(self):
        self._episodes.addItem("Episode 1")
        self._episodes.addItem("Episode 2")
        self._episodes.addItem("Episode 3")
        self._episodes.addItem("Episode 4")
        self._episodes.addItem("Episode 5")
