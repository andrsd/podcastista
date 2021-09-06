from PyQt5 import QtWidgets, QtCore


class SearchThread(QtCore.QThread):
    """ Worker thread for searching """

    def __init__(self, spotify, query):
        super().__init__()
        self._spotify = spotify
        self._query = query
        self._shows = []
        self._episodes = []

    def run(self):
        self._shows = self._spotify.search(
            self._query,
            type='show')

        self._episodes = self._spotify.search(
            self._query,
            type='episode')

    @property
    def shows(self):
        return self._shows

    @property
    def episodes(self):
        return self._episodes



class SearchTab(QtWidgets.QWidget):
    """
    Widget on main window for search
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self.setupWidgets()

    def setupWidgets(self):
        layout = QtWidgets.QVBoxLayout(self)

        self._search_box = QtWidgets.QLineEdit()
        self._search_box.setPlaceholderText("Search")
        self._search_box.setClearButtonEnabled(True)
        self._search_box.returnPressed.connect(self.onSearch)
        self._search_box.textChanged.connect(self.onSearchTextChanged)
        layout.addWidget(self._search_box)

        self._shows_title = QtWidgets.QLabel("Shows")
        layout.addWidget(self._shows_title)

        self._shows = QtWidgets.QListWidget(self)
        self._shows.setFlow(QtWidgets.QListView.LeftToRight)
        self._shows.setMovement(QtWidgets.QListView.Static)
        self._shows.setViewMode(QtWidgets.QListView.IconMode)
        self._shows.setGridSize(QtCore.QSize(100, 120))
        self._shows.setSpacing(4)
        self._shows.setWrapping(True)
        self._shows.itemClicked.connect(self.onShowClicked)
        layout.addWidget(self._shows)

        self._episodes_title = QtWidgets.QLabel("Episodes")
        layout.addWidget(self._episodes_title)

        self._episodes = QtWidgets.QListWidget(self)
        self._episodes.setFlow(QtWidgets.QListView.TopToBottom)
        self._episodes.setMovement(QtWidgets.QListView.Static)
        self._episodes.setViewMode(QtWidgets.QListView.ListMode)
        self._episodes.setGridSize(QtCore.QSize(64, 64))
        self._episodes.itemClicked.connect(self.onEpisodeClicked)
        layout.addWidget(self._episodes)

        self.setLayout(layout)

        self._search_box.setText("Statsthonk")
        # self._search_box.setText("Historie")

    def onSearch(self):
        self._shows.clear()
        self._episodes.clear()

        text = self._search_box.text()

        self._searcher = SearchThread(self._main_window.spotify, text)
        self._searcher.finished.connect(self.onSearchFinished)
        self._searcher.start()

    def onSearchTextChanged(self, text):
        if len(text) == 0:
            self._shows.clear()
            self._episodes.clear()

    def onSearchFinished(self):
        for show in self._searcher.shows['shows']['items']:
            item = QtWidgets.QListWidgetItem(show['name'])
            item.setData(QtCore.Qt.UserRole, show)
            self._shows.addItem(item)

        for episode in self._searcher.episodes['episodes']['items']:
            item = QtWidgets.QListWidgetItem(episode['name'])
            item.setData(QtCore.Qt.UserRole, episode)
            self._episodes.addItem(item)

    def onShowClicked(self, item):
        show = item.data(QtCore.Qt.UserRole)
        self._main_window.viewShow(show['id'])

    def onEpisodeClicked(self, item):
        pass
