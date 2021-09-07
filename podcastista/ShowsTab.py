from PyQt5 import QtWidgets, QtCore
from podcastista.ShowWidget import ShowWidget

class ShowsTab(QtWidgets.QScrollArea):
    """
    Tab on the main window with the list of shows
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent

        self._layout = QtWidgets.QVBoxLayout(self)

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
        for item in shows['items']:
            show = item['show']
            w = ShowWidget(show, self._main_window)
            self._layout.addWidget(w)
        self._layout.addStretch()
