from PyQt5 import QtWidgets, QtCore


class EpisodeWidget(QtWidgets.QWidget):

    DESCRIPTION_HT = 32
    TIME_WD = 100
    LINE_HT = 16

    def __init__(self, episode, parent=None):
        super().__init__(parent)

        self._episode = episode
        self._main_window = parent

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(4)

        left_layout = QtWidgets.QVBoxLayout()

        date = QtCore.QDate.fromString(
            self._episode['release_date'], 'yyyy-MM-dd')
        locale = QtCore.QLocale.system()
        self._date = QtWidgets.QLabel(locale.toString(date))
        self._date.setWordWrap(True)
        self._date.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._date.setFixedHeight(self.LINE_HT)
        font = self._date.font()
        font.setBold(True)
        self._date.setFont(font)
        left_layout.addWidget(self._date)

        left_layout.addSpacing(2)

        self._title = QtWidgets.QLabel(self._episode['name'])
        self._title.setWordWrap(True)
        self._title.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._title.setMaximumHeight(2 * self.LINE_HT)
        font = self._title.font()
        font.setPointSizeF(font.pointSize() * 1.2)
        font.setBold(True)
        self._title.setFont(font)
        left_layout.addWidget(self._title)

        self._description = QtWidgets.QLabel(self._episode['description'])
        self._description.setWordWrap(True)
        self._description.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._description.setMaximumHeight(self.DESCRIPTION_HT)
        self._description.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        left_layout.addWidget(self._description)

        left_layout.addStretch()

        self._layout.addLayout(left_layout)

        self._duration = QtWidgets.QLabel(
            self.msToTime(self._episode['duration_ms']))
        self._duration.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self._duration.setFixedWidth(self.TIME_WD)
        self._duration.setAlignment(QtCore.Qt.AlignCenter)

        self._layout.addWidget(self._duration)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)

    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton and
                self.rect().contains(event.pos())):
            self.onClicked()
        else:
            return super().mouseReleaseEvent(event)

    def onClicked(self):
        pass

    def msToTime(self, ms):
        """ Convert milliseconds to human readable time"""
        return str(int(ms / 1000 / 60)) + " mins"
