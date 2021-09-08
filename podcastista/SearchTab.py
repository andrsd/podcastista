from PyQt5 import QtWidgets, QtCore
from podcastista.ShowWidget import ShowWidget
from podcastista.EpisodeWidget import EpisodeWidget
from podcastista.FlowLayout import FlowLayout


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


class SearchTab(QtWidgets.QScrollArea):
    """
    Widget on main window for search
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent

        self._layout = QtWidgets.QVBoxLayout(self)

        self._search_box = QtWidgets.QLineEdit()
        self._search_box.setPlaceholderText("Search")
        self._search_box.setClearButtonEnabled(True)
        self._search_box.returnPressed.connect(self.onSearch)
        self._search_box.textChanged.connect(self.onSearchTextChanged)
        self._layout.addWidget(self._search_box)

        self._sub_layout = QtWidgets.QVBoxLayout()
        self._layout.addLayout(self._sub_layout)

        self._layout.addStretch()

        widget = QtWidgets.QWidget()
        widget.setLayout(self._layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setWidgetResizable(True)
        self.setWidget(widget)

        self._shows_layout = FlowLayout()
        self._episodes_layout = QtWidgets.QVBoxLayout()

    def onSearch(self):
        text = self._search_box.text()

        self._searcher = SearchThread(self._main_window.spotify, text)
        self._searcher.finished.connect(self.onSearchFinished)
        self._searcher.start()

    def clear(self):
        while self._shows_layout.count() > 0:
            item = self._shows_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        while self._episodes_layout.count() > 0:
            item = self._episodes_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        while self._sub_layout.count() > 0:
            item = self._sub_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

    def onSearchTextChanged(self, text):
        if len(text) == 0:
            self.clear()

    def onSearchFinished(self):
        while self._sub_layout.count() > 0:
            item = self._sub_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        need_hbar = False
        if len(self._searcher.shows['shows']['items']) > 0:
            label = QtWidgets.QLabel("Shows")
            font = label.font()
            font.setBold(True)
            font.setPointSizeF(font.pointSize() * 1.5)
            label.setFont(font)
            self._sub_layout.addWidget(label)

            self._sub_layout.addLayout(self._shows_layout)

            for show in self._searcher.shows['shows']['items']:
                widget = ShowWidget(show, self._main_window)
                self._shows_layout.addWidget(widget)

            need_hbar = True

        if need_hbar:
            hbar = QtWidgets.QFrame()
            hbar.setFrameShape(QtWidgets.QFrame.HLine)
            hbar.setFrameShadow(QtWidgets.QFrame.Plain)
            hbar.setStyleSheet('color: #444')
            self._sub_layout.addWidget(hbar)

        if len(self._searcher.episodes['episodes']['items']) > 0:
            label = QtWidgets.QLabel("Episodes")
            font = label.font()
            font.setBold(True)
            font.setPointSizeF(font.pointSize() * 1.5)
            label.setFont(font)
            self._sub_layout.addWidget(label)

            self._sub_layout.addLayout(self._episodes_layout)

            for episode in self._searcher.episodes['episodes']['items']:
                widget = EpisodeWidget(episode)
                self._episodes_layout.addWidget(widget)

                hbar = QtWidgets.QFrame()
                hbar.setFrameShape(QtWidgets.QFrame.HLine)
                hbar.setFrameShadow(QtWidgets.QFrame.Plain)
                hbar.setStyleSheet('color: #444')
                self._episodes_layout.addWidget(hbar)

            need_hbar = True

    def onEpisodeClicked(self, item):
        pass
