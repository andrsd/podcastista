from PyQt5 import QtWidgets, QtGui, QtCore
from podcastista.assets import Assets


class ShowWidget(QtWidgets.QWidget):

    ARTWORK_WD = 160
    ARTWORK_HT = 160
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

        img_url = self._show['images'][0]['url']
        self._img = Assets().get(img_url)
        self._img.image_loaded.connect(self.onImageLoaded)

        self._layout.addSpacing(8)

        self._title = QtWidgets.QLabel(self._show['name'])
        self._title.setFixedWidth(self.ARTWORK_WD)
        self._title.setFixedHeight(self.LINE_HT)
        font = self._title.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 1.1)
        self._title.setStyleSheet("color: #fff")
        self._title.setFont(font)
        self._layout.addWidget(self._title)

        self._author = QtWidgets.QLabel(self._show['publisher'])
        self._author.setFixedWidth(self.ARTWORK_WD)
        self._author.setFixedHeight(self.LINE_HT)
        self._layout.addWidget(self._author)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "ShowWidget { background-color: #2f2f2f } "
            "ShowWidget:hover { background-color: #363636 }")

    def mouseReleaseEvent(self, event):

        if (event.button() == QtCore.Qt.LeftButton and
                self.rect().contains(event.pos())):
            self.onClicked()
        else:
            return super().mouseReleaseEvent(event)

    def onClicked(self):
        self._main_window.viewShow(self._show['id'])

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._artwork.setPixmap(pixmap)
