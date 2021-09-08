from PyQt5 import QtWidgets, QtCore
from podcastista.ShowWidget import ShowWidget
from podcastista.FlowLayout import FlowLayout


class ShowsTab(QtWidgets.QScrollArea):
    """
    Tab on the main window with the list of shows
    """

    shows_loaded = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self._shows = []

        self._layout = FlowLayout(self)

        widget = QtWidgets.QWidget()
        widget.setLayout(self._layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setWidgetResizable(True)
        self.setWidget(widget)

    @property
    def shows(self):
        return self._shows

    def fill(self):
        if self._main_window.spotify is None:
            return

        self._shows = self._main_window.spotify.current_user_saved_shows()
        for item in self._shows['items']:
            show = item['show']
            w = ShowWidget(show, self._main_window)
            self._layout.addWidget(w)

        self.shows_loaded.emit(self._shows)
