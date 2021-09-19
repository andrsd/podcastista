from PyQt5 import QtWidgets, QtGui, QtCore
from podcastista.assets import Assets
from podcastista import utils
from podcastista.ClickableLabel import ClickableLabel


class ShowEpisodeWidget(QtWidgets.QWidget):

    ARTWORK_WD = 220
    ARTWORK_HT = 220
    LINE_HT = 16
    SPACE = 4

    def __init__(self, show, parent=None):
        super().__init__(parent)
        self._show = show
        self._main_window = parent

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(6)

        self._artwork = QtWidgets.QLabel()
        self._artwork.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._artwork.setFixedSize(self.ARTWORK_WD, self.ARTWORK_HT)
        self._layout.addWidget(self._artwork)

        images = self._show['images']
        img_url = None
        for img in images:
            if (img['height'] >= self.ARTWORK_HT and img['height'] <= 600):
                img_url = img['url']
        self._img = Assets().get(img_url)
        self._img.image_loaded.connect(self.onImageLoaded)

        self._layout.addSpacing(8)

        self._episode = self._show['episodes'][0]

        self._date = QtWidgets.QLabel(
            utils.dateToStr(self._episode['release_date']))
        self._date.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._date.setFixedWidth(self.ARTWORK_WD)
        self._date.setFixedHeight(self.LINE_HT)
        font = self._date.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 0.9)
        font.setCapitalization(QtGui.QFont.AllUppercase)
        self._date.setFont(font)
        self._date.setStyleSheet("color: #888")
        self._layout.addWidget(self._date)

        self._episode_name = ClickableLabel(self._episode['name'])
        self._episode_name.setWordWrap(True)
        self._episode_name.setFixedWidth(self.ARTWORK_WD)
        self._episode_name.setFixedHeight(62)
        self._episode_name.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        font = self._episode_name.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 1.3)
        self._episode_name.setFont(font)
        self._episode_name.setStyleSheet("color: #fff")
        self._episode_name.clicked.connect(self.onEpisodeNameClicked)
        self._layout.addWidget(self._episode_name)

        self._title = ClickableLabel(self._show['name'])
        self._title.setFixedWidth(self.ARTWORK_WD)
        self._title.setFixedHeight(self.LINE_HT)
        self._title.setStyleSheet("color: #307BF6")
        self._title.clicked.connect(self.onTitleClicked)
        self._layout.addWidget(self._title)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "ShowEpisodeWidget { background-color: #2f2f2f } "
            "ShowEpisodeWidget:hover { background-color: #363636 }")

    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton and
                self.rect().contains(event.pos())):
            self.onClicked()
        else:
            return super().mouseReleaseEvent(event)

    def onClicked(self):
        self._main_window.viewEpisode(self._episode)

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._artwork.setPixmap(pixmap)

    def onEpisodeNameClicked(self):
        self._main_window.viewEpisode(self._episode)

    def onTitleClicked(self):
        self._main_window.viewShow(self._show['id'])
