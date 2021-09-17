from PyQt5 import QtWidgets, QtCore, QtGui
from podcastista.assets import Assets
from podcastista.EpisodeWidget import EpisodeWidget
from podcastista.HLine import HLine
from podcastista.BackButton import BackButton
from podcastista.SubsectionTitle import SubsectionTitle
from podcastista.InfoLabel import InfoLabel
from podcastista import utils


class ShowDetails(QtWidgets.QWidget):
    """
    Widget on main window with show details
    """

    ARTWORK_WD = 200
    ARTWORK_HT = 200

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self._show = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setContentsMargins(4, 4, 4, 4)

        self._back = BackButton()
        self._back.clicked.connect(self.onBack)
        top_layout.addWidget(self._back)

        self._show_label = QtWidgets.QLabel()
        self._show_label.setAlignment(QtCore.Qt.AlignCenter)
        self._show_label.setStyleSheet("""
            font-weight: bold;
            """)
        top_layout.addWidget(self._show_label)

        layout.addLayout(top_layout)

        scroll_layout = QtWidgets.QVBoxLayout()
        scroll_layout.setSpacing(8)
        scroll_layout.setContentsMargins(0, 0, 16, 16)

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

        button_layout = QtWidgets.QHBoxLayout()
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
        button_layout.addWidget(self._play_latest)

        button_layout.addStretch()

        self._follow_button = QtWidgets.QPushButton("")
        css = """
            QPushButton {
                border-radius: 4px;
                background-color: #282828;
                border: 2px solid #888;
                font-size: 13px;
                font-weight: bold;
                text-transform: uppercase;
                color: #C8C8C8;
            }
            QPushButton:hover {
                border-color: #C8C8C8;
            }
            """
        self._follow_button.setFlat(True)
        self._follow_button.setStyleSheet(css)
        self._follow_button.setFixedWidth(120)
        self._follow_button.setFixedHeight(28)
        self._follow_button.setContentsMargins(0, 0, 0, 0)
        self._follow_button.clicked.connect(self.onFollowClicked)
        button_layout.addWidget(self._follow_button)

        banner_right_layout.addLayout(button_layout)

        banner_h_layout.addLayout(banner_right_layout)

        banner = QtWidgets.QWidget()
        banner.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        banner.setLayout(banner_h_layout)
        scroll_layout.addWidget(banner)

        hline = HLine()
        hline.setStyleSheet(
            "margin-left: 38px; "
            "margin-right: 28px; "
            "color: #444;")
        scroll_layout.addWidget(hline)

        self._episodes_label = SubsectionTitle("Episodes")
        self._episodes_label.setStyleSheet("margin-left: 36px")
        scroll_layout.addWidget(self._episodes_label)

        self._episodes_layout = QtWidgets.QVBoxLayout()
        self._episodes_layout.setContentsMargins(0, 0, 0, 0)
        self._episodes_layout.setSpacing(0)

        scroll_layout.addLayout(self._episodes_layout)

        self._see_all_episodes = QtWidgets.QPushButton("")
        self._see_all_episodes.setStyleSheet("""
            QPushButton {
                font-size: 13px;
                margin-left: 38px;
            }
            QPushButton:hover {
                color: #307BF6;
            }
            """)
        self._see_all_episodes.setFlat(True)
        self._see_all_episodes.setFixedHeight(28)
        self._see_all_episodes.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed)
        scroll_layout.addWidget(self._see_all_episodes)

        hline = HLine()
        hline.setStyleSheet(
            "margin-left: 38px; "
            "margin-right: 28px; "
            "color: #444")
        scroll_layout.addWidget(hline)

        scroll_layout.addSpacing(8)

        self._info_label = SubsectionTitle("Information")
        self._info_label.setStyleSheet("margin-left: 36px")
        scroll_layout.addWidget(self._info_label)

        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(28, 0, 16, 0)

        self._publisher_info = InfoLabel("Publisher")
        grid.addWidget(self._publisher_info, 0, 0)

        self._episodes_info = InfoLabel("Episodes")
        grid.addWidget(self._episodes_info, 0, 1)

        self._rating_info = InfoLabel("Rating")
        grid.addWidget(self._rating_info, 1, 0)

        self._language_info = InfoLabel("Language")
        grid.addWidget(self._language_info, 1, 1)

        scroll_layout.addLayout(grid)

        widget = QtWidgets.QWidget()
        widget.setLayout(scroll_layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)

        scroll_layout.addStretch()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)
        scroll_area.verticalScrollBar().valueChanged.connect(self.onVertScroll)

        layout.addWidget(scroll_area)

    @property
    def id(self):
        if self._show is None:
            return None
        else:
            return self._show['id']

    def fill(self, show_id):
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

        for episode in self._show['episodes']['items'][0:8]:
            widget = EpisodeWidget(episode, parent=self._main_window)
            self._episodes_layout.addWidget(widget)

            hline = HLine()
            hline.setStyleSheet(
                "margin-left: 38px; "
                "margin-right: 28px; "
                "color: #444")
            self._episodes_layout.addWidget(hline)

        self.updateFollowState()

        self._see_all_episodes.setText(
            "See all {} Episodes".format(self._show['total_episodes']))

        self._publisher_info.set(self._show['publisher'])
        self._episodes_info.set(str(self._show['total_episodes']))
        langs = []
        for l in self._show['languages']:
            locale = QtCore.QLocale(l)
            langs.append(QtCore.QLocale.languageToString(locale.language()))
        self._language_info.set(", ".join(langs))
        self._rating_info.set(utils.rating(self._show['explicit']))

    def onBack(self):
        self._main_window.onBack()

    def updateFollowState(self):
        show_id = self._show['id']
        res = self._main_window.spotify.current_user_saved_shows_contains(
            [show_id])
        self._following = res[0]

        if self._following:
            text = "Following"
        else:
            text = "Follow"
        self._follow_button.setText(text)

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._show_artwork.setPixmap(pixmap)

    def onFollowClicked(self):
        if self._following:
            self._main_window.unfollowShow(self._show['id'])
        else:
            self._main_window.followShow(self._show['id'])
        self.updateFollowState()

    def onVertScroll(self, value):
        if value > 80:
            self._show_label.setText(self._show['name'])
            clr2 = QtGui.QColor("#C8C8C8")

            if value < 100:
                t = (float(value) - 80) / 20
                clr = QtGui.QColor.fromRgbF(
                    clr2.redF(),
                    clr2.greenF(),
                    clr2.blueF(),
                    t)
            else:
                clr = clr2

            qss = """
                font-weight: bold;
                color: {};
                """.format(clr.name(QtGui.QColor.HexArgb))
            self._show_label.setStyleSheet(qss)
        else:
            self._show_label.setText("")
