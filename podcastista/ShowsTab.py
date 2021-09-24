from PyQt5 import QtWidgets, QtCore
from podcastista.ShowWidget import ShowWidget
from podcastista.FlowLayout import FlowLayout


class ShowsTab(QtWidgets.QWidget):
    """
    Tab on the main window with the list of shows
    """

    shows_loaded = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self._shows = []

        # empty widget
        self._empty_widget = QtWidgets.QWidget()
        empty_layout = QtWidgets.QVBoxLayout()

        nothing = QtWidgets.QLabel("No shows")
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

        # list of shows
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

    @property
    def shows(self):
        return self._shows

    def clear(self):
        self._stacked_layout.setCurrentWidget(self._empty_widget)

        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

    def fill(self):
        if self._main_window.spotify is None:
            return

        self._shows = self._main_window.spotify.current_user_saved_shows()
        for item in self._shows['items']:
            show = item['show']
            w = ShowWidget(show, self._main_window)
            self._layout.addWidget(w)

        if self._layout.count() > 0:
            self._stacked_layout.setCurrentWidget(self._list)

        self.shows_loaded.emit(self._shows)
