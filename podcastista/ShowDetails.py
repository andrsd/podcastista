from PyQt5 import QtWidgets, QtCore, QtNetwork, QtGui


class ShowDetails(QtWidgets.QWidget):
    """
    Widget on main window with show details
    """

    ARTWORK_WD = 192
    ARTWORK_HT = 192

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self.setupWidgets()
        self._follow_button = None

        self._nam = QtNetwork.QNetworkAccessManager()
        self._nam.finished.connect(self.onNetworkReply)

    def setupWidgets(self):
        sa_layout = QtWidgets.QVBoxLayout(self)

        self._w = QtWidgets.QWidget()
        self._w.setLayout(sa_layout)
        self._w.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self._w)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def setShow(self, show_id):
        show = self._main_window.spotify.show(show_id)

        sa_layout = self._w.layout()
        while sa_layout.count() > 0:
            item = sa_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        self._back = QtWidgets.QPushButton("Back")
        self._back.clicked.connect(self.onBack)
        sa_layout.addWidget(self._back)

        banner_h_layout = QtWidgets.QHBoxLayout()
        banner_h_layout.setContentsMargins(0, 0, 0, 0)

        self._show_artwork = QtWidgets.QLabel()
        self._show_artwork.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._show_artwork.setFixedSize(self.ARTWORK_WD, self.ARTWORK_HT)
        banner_h_layout.addWidget(self._show_artwork)

        images = show['images']
        img_url = None
        for img in images:
            if (img['height'] >= self.ARTWORK_HT and img['height'] <= 600):
                img_url = img['url']
        img_req = QtNetwork.QNetworkRequest(QtCore.QUrl(img_url))
        self._nam.get(img_req)

        banner_right_layout = QtWidgets.QVBoxLayout()

        self._show_title = QtWidgets.QLabel(show['name'])
        font = self._show_title.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 2)
        self._show_title.setFont(font)
        banner_right_layout.addWidget(self._show_title)

        self._show_author = QtWidgets.QLabel(show['publisher'])
        font = self._show_author.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 1.2)
        self._show_author.setFont(font)
        banner_right_layout.addWidget(self._show_author)

        self._show_description = QtWidgets.QLabel(show['description'])
        banner_right_layout.addWidget(self._show_description)

        banner_right_layout.addStretch()

        self._follow_button = QtWidgets.QPushButton("Follow")
        self._follow_button.clicked.connect(self.onFollow)
        banner_right_layout.addWidget(self._follow_button)

        banner_h_layout.addLayout(banner_right_layout)

        banner = QtWidgets.QWidget()
        banner.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        banner.setFixedHeight(self.ARTWORK_HT)
        banner.setLayout(banner_h_layout)
        sa_layout.addWidget(banner)

        hbar = QtWidgets.QFrame()
        hbar.setFrameShape(QtWidgets.QFrame.HLine)
        hbar.setFrameShadow(QtWidgets.QFrame.Plain)
        sa_layout.addWidget(hbar)

        self._episodes_label = QtWidgets.QLabel("Episodes")
        font = self._episodes_label.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 1.5)
        self._episodes_label.setFont(font)
        sa_layout.addWidget(self._episodes_label)

        for episode in show['episodes']['items']:
            label = QtWidgets.QLabel(episode['name'])
            sa_layout.addWidget(label)

        sa_layout.addStretch()

    def onNetworkReply(self, reply):
        """
        Called when network request was finished
        """
        if reply.url().host() == "localhost":
            # our own requests
            return
        else:
            img = QtGui.QImage()
            img.load(reply, "")
            scaled_img = img.scaledToWidth(self.ARTWORK_WD)
            pixmap = QtGui.QPixmap.fromImage(scaled_img)
            self._show_artwork.setPixmap(pixmap)

    def onBack(self, item):
        self._main_window.viewMain()

    def onFollow(self):
        pass
