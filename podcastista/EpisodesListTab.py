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


class EpisodesListTab(QtWidgets.QScrollArea):
    """
    Tab on the main window with the list of episodes
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setSpacing(0)

        widget = QtWidgets.QWidget()
        widget.setLayout(self._layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setWidgetResizable(True)
        self.setWidget(widget)

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

        for episode in sorted_episodes:
            # filter out played episodes
            display = True
            if ('resume_point' in episode and
                    episode['resume_point']['fully_played']):
                display = False

            if display:
                w = EpisodeWidget(
                    episode,
                    artwork=True,
                    parent=self._main_window)
                self._layout.addWidget(w)

                hline = HLine()
                hline.setStyleSheet(
                    "margin-left: 16px; "
                    "margin-right: 16px; "
                    "color: #444")
                self._layout.addWidget(hline)
