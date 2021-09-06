from PyQt5 import QtWidgets, QtCore


class ShowsTab(QtWidgets.QWidget):
    """
    Tab on the main window with the list of shows
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self.setupWidgets()
        self.fillShows()

    def setupWidgets(self):
        layout = QtWidgets.QVBoxLayout(self)

        self._title = QtWidgets.QLabel("Shows")
        layout.addWidget(self._title)

        self._shows = QtWidgets.QListWidget(self)
        self._shows.setFlow(QtWidgets.QListView.LeftToRight)
        self._shows.setMovement(QtWidgets.QListView.Static)
        self._shows.setViewMode(QtWidgets.QListView.IconMode)
        self._shows.setGridSize(QtCore.QSize(100, 120))
        self._shows.setSpacing(4)
        self._shows.setWrapping(True)
        self._shows.itemClicked.connect(self.onItemClicked)
        layout.addWidget(self._shows)

        self.setLayout(layout)

    def fillShows(self):
        self._shows.addItem("Podcast 1")
        self._shows.addItem("Podcast 2")

    def onItemClicked(self, item):
        self._main_window.viewShow(item.text())
