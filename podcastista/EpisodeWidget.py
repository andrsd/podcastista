from PyQt5 import QtWidgets, QtCore, QtGui
from podcastista.assets import Assets


class EpisodeWidget(QtWidgets.QWidget):

    ARTWORK_HT = 100
    ARTWORK_WD = 100
    DESCRIPTION_HT = 32
    TIME_WD = 100
    LINE_HT = 16

    def __init__(self, episode, artwork=False, parent=None):
        super().__init__(parent)

        self._episode = episode
        self._main_window = parent

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(4)

        self._played = False
        if ('resume_point' in episode and
                episode['resume_point']['fully_played']):
            self._played = True

        if artwork:
            self._artwork = QtWidgets.QLabel()
            self._artwork.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self._artwork.setFixedSize(self.ARTWORK_WD, self.ARTWORK_HT)
            self._artwork.setStyleSheet("border: 1px solid #fff")
            self._layout.addWidget(self._artwork)

            images = self._episode['images']
            img_url = None
            for img in images:
                if (img['height'] >= self.ARTWORK_HT and img['height'] <= 600):
                    img_url = img['url']
            self._img = Assets().get(img_url)
            self._img.image_loaded.connect(self.onImageLoaded)

            self._layout.addSpacing(8)
        else:
            self._artwork = None
            self._img = None

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
        font.setCapitalization(QtGui.QFont.AllUppercase)
        font.setPointSizeF(font.pointSize() * 0.9)
        self._date.setFont(font)
        self._date.setStyleSheet("color: #888")
        left_layout.addWidget(self._date)

        left_layout.addSpacing(2)

        self._title = QtWidgets.QLabel(self._episode['name'])
        self._title.setWordWrap(True)
        self._title.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._title.setMaximumHeight(2 * self.LINE_HT)
        font = self._title.font()
        font.setPointSizeF(font.pointSize() * 1.2)
        if not self._played:
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
        self._description.setStyleSheet("color: #888")
        left_layout.addWidget(self._description)

        left_layout.addStretch()

        self._layout.addLayout(left_layout)

        if self._played:
            time = "Played"
        else:
            time = self.msToTime(self._episode['duration_ms'])
        self._duration = QtWidgets.QLabel(time)
        self._duration.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self._duration.setFixedWidth(self.TIME_WD)
        self._duration.setAlignment(QtCore.Qt.AlignCenter)

        self._layout.addWidget(self._duration)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "EpisodeWidget { background-color: #282828 } "
            "EpisodeWidget:hover { background-color: #363636 }")

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
        secs = int(ms / 1000)
        mins = int(secs / 60)
        if mins < 60:
            return str(int(ms / 1000 / 60)) + " mins"
        else:
            hrs = int(mins / 60)
            mins = int(mins % 60)
            return str(hrs) + "h " + str(mins) + "m"

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._artwork.setPixmap(pixmap)
