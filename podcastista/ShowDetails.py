from PyQt5 import QtWidgets, QtCore, QtGui
from podcastista.assets import Assets
from podcastista.EpisodeWidget import EpisodeWidget
from podcastista.HLine import HLine


class ShowDetails(QtWidgets.QScrollArea):
    """
    Widget on main window with show details
    """

    ARTWORK_WD = 200
    ARTWORK_HT = 200

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self._show = None
        self._follow_button = None

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(16, 16, 16, 16)
        widget = QtWidgets.QWidget()
        widget.setLayout(self._layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setWidgetResizable(True)
        self.setWidget(widget)

    def setShow(self, show_id):
        self._show = self._main_window.spotify.show(show_id)

        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        self._back = QtWidgets.QPushButton("Back")
        self._back.clicked.connect(self.onBack)
        self._layout.addWidget(self._back)

        banner_h_layout = QtWidgets.QHBoxLayout()
        banner_h_layout.setContentsMargins(16, 16, 16, 16)

        self._show_artwork = QtWidgets.QLabel()
        self._show_artwork.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._show_artwork.setFixedSize(self.ARTWORK_WD, self.ARTWORK_HT)
        banner_h_layout.addWidget(self._show_artwork)

        images = self._show['images']
        img_url = None
        for img in images:
            if (img['height'] >= self.ARTWORK_HT and img['height'] <= 300):
                img_url = img['url']
        self._img = Assets().get(img_url)
        self._img.image_loaded.connect(self.onImageLoaded)

        banner_right_layout = QtWidgets.QVBoxLayout()
        banner_right_layout.setSpacing(2)

        banner_right_layout.addStretch()

        self._show_title = QtWidgets.QLabel(self._show['name'])
        self._show_title.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self._show_title.setWordWrap(True)
        self._show_title.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        font = self._show_title.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 2)
        self._show_title.setFont(font)
        banner_right_layout.addWidget(self._show_title)

        self._show_author = QtWidgets.QLabel(self._show['publisher'])
        self._show_author.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._show_author.setFixedHeight(20)
        font = self._show_author.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 1.2)
        self._show_author.setFont(font)
        banner_right_layout.addWidget(self._show_author)

        # self._show_description = QtWidgets.QLabel(self._show['description'])
        # self._show_description.setAlignment(
        #     QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        # self._show_description.setSizePolicy(
        #     QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # banner_right_layout.addWidget(self._show_description)

        # banner_right_layout.addStretch()

        # self._follow_button = QtWidgets.QPushButton("Follow")
        # self._follow_button.clicked.connect(self.onFollow)
        # banner_right_layout.addWidget(self._follow_button)
        # self.updateFollowButton()

        banner_h_layout.addLayout(banner_right_layout)

        banner = QtWidgets.QWidget()
        banner.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        banner.setLayout(banner_h_layout)
        self._layout.addWidget(banner)

        self._layout.addWidget(HLine())

        self._episodes_label = QtWidgets.QLabel("Episodes")
        self._episodes_label.setStyleSheet("margin-left: 12px")
        font = self._episodes_label.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 1.5)
        self._episodes_label.setFont(font)
        self._layout.addWidget(self._episodes_label)

        self._episodes_layout = QtWidgets.QVBoxLayout()
        self._episodes_layout.setContentsMargins(0, 0, 0, 0)
        self._episodes_layout.setSpacing(0)

        for episode in self._show['episodes']['items']:
            widget = EpisodeWidget(episode)
            self._episodes_layout.addWidget(widget)

            hline = HLine()
            hline.setStyleSheet("margin-left: 16px; margin-right: 16px; color: #444")
            self._episodes_layout.addWidget(hline)

        self._layout.addLayout(self._episodes_layout)
        self._layout.addStretch()

    def onBack(self, item):
        self._main_window.viewMain()

    def onFollow(self):
        self._main_window.followShow(self._show['id'])
        self.updateFollowButton()

    def updateFollowButton(self):
        self._follow_button.setEnabled(False)

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._show_artwork.setPixmap(pixmap)
