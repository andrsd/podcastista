from PyQt5 import QtWidgets, QtCore, QtGui
from podcastista.assets import Assets
from podcastista.EpisodeWidget import EpisodeWidget
from podcastista.HLine import HLine
from podcastista.BackButton import BackButton
from podcastista.SubsectionTitle import SubsectionTitle


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

        self._top_layout = QtWidgets.QVBoxLayout(self)
        self._top_layout.setSpacing(0)
        self._top_layout.setContentsMargins(4, 8, 4, 0)

        self._back = BackButton()
        self._back.clicked.connect(self.onBack)
        self._top_layout.addWidget(self._back)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(8)
        self._layout.setContentsMargins(0, 0, 16, 16)
        self._top_layout.addLayout(self._layout)
        self._top_layout.addStretch()

        banner_h_layout = QtWidgets.QHBoxLayout()
        banner_h_layout.setContentsMargins(40, 16, 30, 16)
        banner_h_layout.setSpacing(40)

        self._show_artwork = QtWidgets.QLabel()
        self._show_artwork.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._show_artwork.setFixedSize(self.ARTWORK_WD, self.ARTWORK_HT)
        banner_h_layout.addWidget(self._show_artwork)

        banner_right_layout = QtWidgets.QVBoxLayout()
        banner_right_layout.setSpacing(0)

        banner_right_layout.addSpacing(25)

        self._show_title = QtWidgets.QLabel()
        self._show_title.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self._show_title.setWordWrap(True)
        self._show_title.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        font = self._show_title.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 2)
        self._show_title.setFont(font)
        banner_right_layout.addWidget(self._show_title)

        self._show_author = QtWidgets.QLabel()
        self._show_author.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._show_author.setFixedHeight(20)
        font = self._show_author.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 1.2)
        self._show_author.setFont(font)
        banner_right_layout.addWidget(self._show_author)

        banner_right_layout.addSpacing(25)
        self._latest_episode = QtWidgets.QLabel()
        self._latest_episode.setWordWrap(True)
        self._latest_episode.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._latest_episode.setStyleSheet("""
            font-size: 14px;
            """)
        self._latest_episode.setFixedHeight(50)
        self._latest_episode.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        banner_right_layout.addWidget(self._latest_episode)

        banner_right_layout.addSpacing(25)

        self._play_latest = QtWidgets.QPushButton("\u25B6  Latest Episode")
        css = """
            border-radius: 4px;
            background-color: #307BF6;
            border: none;
            """
        self._play_latest.setFlat(True)
        self._play_latest.setStyleSheet(css)
        self._play_latest.setFixedWidth(150)
        self._play_latest.setFixedHeight(28)
        self._play_latest.setContentsMargins(0, 0, 0, 0)
        font = self._play_latest.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 1.1)
        self._play_latest.setFont(font)
        banner_right_layout.addWidget(self._play_latest)

        banner_h_layout.addLayout(banner_right_layout)

        banner = QtWidgets.QWidget()
        banner.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        banner.setLayout(banner_h_layout)
        self._layout.addWidget(banner)

        hline = HLine()
        hline.setStyleSheet(
            "margin-left: 38px; "
            "margin-right: 28px; "
            "color: #444;")
        self._layout.addWidget(hline)

        self._episodes_label = SubsectionTitle("Episodes")
        self._episodes_label.setStyleSheet("margin-left: 36px")
        self._layout.addWidget(self._episodes_label)

        self._episodes_layout = QtWidgets.QVBoxLayout()
        self._episodes_layout.setContentsMargins(0, 0, 0, 0)
        self._episodes_layout.setSpacing(0)

        self._layout.addLayout(self._episodes_layout)

        widget = QtWidgets.QWidget()
        widget.setLayout(self._top_layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setWidgetResizable(True)
        self.setWidget(widget)

    @property
    def id(self):
        if self._show is None:
            return None
        else:
            return self._show['id']

    def setShow(self, show_id):
        self._show = self._main_window.spotify.show(show_id)

        while self._episodes_layout.count() > 0:
            item = self._episodes_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        images = self._show['images']
        img_url = None
        for img in images:
            if (img['height'] >= self.ARTWORK_HT and img['height'] <= 300):
                img_url = img['url']
        self._img = Assets().get(img_url)
        self._img.image_loaded.connect(self.onImageLoaded)

        self._show_title.setText(self._show['name'])
        self._show_author.setText(self._show['publisher'])

        latest_episode = self._show['episodes']['items'][0]
        self._latest_episode.setText(
            ": ".join([latest_episode['name'], latest_episode['description']])
        )

        for episode in self._show['episodes']['items']:
            widget = EpisodeWidget(episode, parent=self._main_window)
            self._episodes_layout.addWidget(widget)

            hline = HLine()
            hline.setStyleSheet(
                "margin-left: 38px; "
                "margin-right: 28px; "
                "color: #444")
            self._episodes_layout.addWidget(hline)

    def onBack(self):
        self._main_window.onBack()

    def onFollow(self):
        self._main_window.followShow(self._show['id'])
        self.updateFollowButton()

    def updateFollowButton(self):
        self._follow_button.setEnabled(False)

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._show_artwork.setPixmap(pixmap)
