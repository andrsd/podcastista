from PyQt5 import QtWidgets, QtCore
from podcastista.ShowWidget import ShowWidget
from podcastista.EpisodeWidget import EpisodeWidget
from podcastista.FlowLayout import FlowLayout
from podcastista.HLine import HLine


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

    def search(self, text):
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

        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

    def onSearchFinished(self):
        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        need_hbar = False
        if len(self._searcher.shows['shows']['items']) > 0:
            label = QtWidgets.QLabel("Shows")
            font = label.font()
            font.setBold(True)
            font.setPointSizeF(font.pointSize() * 1.5)
            label.setFont(font)
            self._layout.addWidget(label)

            self._layout.addLayout(self._shows_layout)

            for show in self._searcher.shows['shows']['items']:
                widget = ShowWidget(show, self._main_window)
                self._shows_layout.addWidget(widget)

            need_hbar = True

        if need_hbar:
            self._layout.addWidget(HLine())

        if len(self._searcher.episodes['episodes']['items']) > 0:
            label = QtWidgets.QLabel("Episodes")
            font = label.font()
            font.setBold(True)
            font.setPointSizeF(font.pointSize() * 1.5)
            label.setFont(font)
            self._layout.addWidget(label)

            self._layout.addLayout(self._episodes_layout)

            for episode in self._searcher.episodes['episodes']['items']:
                if episode is not None:
                    widget = EpisodeWidget(episode, parent=self._main_window)
                    self._episodes_layout.addWidget(widget)

                    self._episodes_layout.addWidget(HLine())

            need_hbar = True
