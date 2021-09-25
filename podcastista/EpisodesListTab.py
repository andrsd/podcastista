from PyQt5 import QtWidgets, QtCore
from podcastista.EpisodeWidget import EpisodeWidget
from podcastista.HLine import HLine


class FillThread(QtCore.QThread):
    """ Worker thread for loading up episodes """

    def __init__(self, spotify, shows):
        super().__init__()
        self._spotify = spotify
        self._shows = shows
        self._episodes = []

    def run(self):
        self._episodes = []
        for item in self._shows['items']:
            show = item['show']

            show_episodes = self._spotify.show_episodes(show['id'], limit=20)
            for episode in show_episodes['items']:
                self._episodes.append(episode)

    @property
    def episodes(self):
        return self._episodes


class EpisodesListTab(QtWidgets.QWidget):
    """
    Tab on the main window with the list of episodes
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self._episode_idx = {}
        self._episodes = []

        # empty widget
        self._empty_widget = QtWidgets.QWidget()
        empty_layout = QtWidgets.QVBoxLayout()

        nothing = QtWidgets.QLabel("No episodes")
        nothing.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        nothing.setContentsMargins(40, 20, 40, 20)
        nothing.setStyleSheet("""
            font-size: 14px;
            """)
        nothing.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        empty_layout.addWidget(nothing)
        empty_layout.addStretch(1)
        self._empty_widget.setLayout(empty_layout)

        # list of episodes

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(4, 16, 16, 16)

        widget = QtWidgets.QWidget()
        widget.setLayout(self._layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)

        self._list = QtWidgets.QScrollArea()
        self._list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._list.setWidgetResizable(True)
        self._list.setWidget(widget)

        self._stacked_layout = QtWidgets.QStackedLayout(self)
        self._stacked_layout.addWidget(self._empty_widget)
        self._stacked_layout.addWidget(self._list)

    def clear(self):
        self._stacked_layout.setCurrentWidget(self._empty_widget)

        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

    def fill(self, shows):
        if self._main_window.spotify is None:
            return

        self._filler = FillThread(self._main_window.spotify, shows)
        self._filler.finished.connect(self.onFillFinished)
        self._filler.start()

    def onFillFinished(self):
        sorted_episodes = sorted(
            self._filler.episodes,
            key=lambda k: k['release_date'],
            reverse=True)

        self._episode_idx = {}
        self._episodes = []
        idx = 0
        for episode in sorted_episodes:
            # filter out played episodes
            display = True
            if ('resume_point' in episode and
                    episode['resume_point']['fully_played']):
                display = False

            if display:
                self._episodes.append(episode)
                self._episode_idx[episode['id']] = idx
                idx = idx + 1
                w = EpisodeWidget(
                    episode,
                    artwork=True,
                    parent=self._main_window)
                w.play.connect(self.onPlayFromEpisode)
                self._layout.addWidget(w)

                hline = HLine()
                hline.setStyleSheet(
                    "margin-left: 38px; "
                    "margin-right: 38px; "
                    "color: #444")
                self._layout.addWidget(hline)

        if self._layout.count() > 0:
            self._stacked_layout.setCurrentWidget(self._list)

    def onPlayFromEpisode(self, episode):
        start_idx = self._episode_idx[episode['id']]
        uris = []
        for ep in self._episodes[start_idx:]:
            uris.append(ep['uri'])
        self._main_window.startPlayback(uris)
