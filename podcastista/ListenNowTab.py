from PyQt5 import QtWidgets, QtCore
from podcastista.ShowEpisodeWidget import ShowEpisodeWidget
from podcastista.FlowLayout import FlowLayout


class FillThread(QtCore.QThread):
    """ Worker thread for loading up episodes """

    def __init__(self, spotify, shows):
        super().__init__()
        self._spotify = spotify
        self._shows = shows

    def run(self):
        for item in self._shows['items']:
            show = item['show']
            show['episodes'] = []

            show_episodes = self._spotify.show_episodes(show['id'], limit=20)
            for episode in show_episodes['items']:
                display = True
                if ('resume_point' in episode and
                        episode['resume_point']['fully_played']):
                    display = False
                if display:
                    show['episodes'].append(episode)

    @property
    def shows(self):
        return self._shows


class ListenNowTab(QtWidgets.QScrollArea):
    """
    Tab on the main window with the list of shows
    """

    shows_loaded = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent

        self._layout = FlowLayout(self)

        widget = QtWidgets.QWidget()
        widget.setLayout(self._layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setWidgetResizable(True)
        self.setWidget(widget)

    def fill(self):
        if self._main_window.spotify is None:
            return

        shows = self._main_window.spotify.current_user_saved_shows()
        self._filler = FillThread(self._main_window.spotify, shows)
        self._filler.finished.connect(self.onFillFinished)
        self._filler.start()

    def onFillFinished(self):
        for item in self._filler.shows['items']:
            show = item['show']
            if len(show['episodes']) > 0:
                w = ShowEpisodeWidget(show, self._main_window)
                self._layout.addWidget(w)
