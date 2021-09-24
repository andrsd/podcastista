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


class ListenNowTab(QtWidgets.QWidget):
    """
    Tab on the main window with the list of shows
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent

        # empty widget
        self._empty_widget = QtWidgets.QWidget()
        empty_layout = QtWidgets.QVBoxLayout()

        nothing = QtWidgets.QLabel("No items")
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

        # list of items

        self._layout = FlowLayout()

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

        if self._layout.count() > 0:
            self._stacked_layout.setCurrentWidget(self._list)
