from PyQt5 import QtWidgets, QtCore, QtGui
from podcastista.assets import Assets
from podcastista.EpisodeWidget import EpisodeWidget
from podcastista.HLine import HLine
from podcastista.BackButton import BackButton
from podcastista.SubsectionTitle import SubsectionTitle
from podcastista.InfoLabel import InfoLabel
from podcastista.ClickableLabel import ClickableLabel
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
        self._episode_idx = {}

        # top section
        self._back = BackButton()
        self._back.clicked.connect(self.onBack)

        self._show_label = QtWidgets.QLabel()
        self._show_label.setAlignment(QtCore.Qt.AlignCenter)
        self._show_label.setStyleSheet("""
            font-weight: bold;
            """)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setContentsMargins(4, 4, 4, 4)
        top_layout.addWidget(self._back)
        top_layout.addWidget(self._show_label)

        # show info widgets
        info_layout = QtWidgets.QVBoxLayout()
        info_layout.setSpacing(8)
        info_layout.setContentsMargins(0, 0, 16, 16)

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
            font-weight: bold;
            font-size: 14px;
            """
        self._play_latest.setFlat(True)
        self._play_latest.setStyleSheet(css)
        self._play_latest.setFixedWidth(150)
        self._play_latest.setFixedHeight(28)
        self._play_latest.setContentsMargins(0, 0, 0, 0)
        self._play_latest.setEnabled(False)
        self._play_latest.clicked.connect(self.onPlayLatest)
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
        info_layout.addWidget(banner)

        hline = HLine()
        hline.setStyleSheet(
            "margin-left: 38px; "
            "margin-right: 28px; "
            "color: #444;")
        info_layout.addWidget(hline)

        self._episodes_label = SubsectionTitle("Episodes")
        self._episodes_label.setStyleSheet("margin-left: 32px")
        info_layout.addWidget(self._episodes_label)

        self._episodes_layout = QtWidgets.QVBoxLayout()
        self._episodes_layout.setContentsMargins(0, 0, 0, 0)
        self._episodes_layout.setSpacing(0)

        info_layout.addLayout(self._episodes_layout)

        see_all_layout = QtWidgets.QHBoxLayout()
        see_all_layout.addSpacing(38)

        self._see_all_episodes = ClickableLabel("")
        self._see_all_episodes.setContentsMargins(0, 4, 0, 4)
        self._see_all_episodes.setStyleSheet("""
            color: #307BF6;
            """)
        self._see_all_episodes.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed)
        self._see_all_episodes.clicked.connect(self.onSeeAllEpisodes)
        see_all_layout.addWidget(self._see_all_episodes)

        see_all_layout.addStretch()

        info_layout.addLayout(see_all_layout)

        hline = HLine()
        hline.setStyleSheet(
            "margin-left: 38px; "
            "margin-right: 28px; "
            "color: #444")
        info_layout.addWidget(hline)

        info_layout.addSpacing(8)

        self._info_label = SubsectionTitle("Information")
        self._info_label.setStyleSheet("margin-left: 32px")
        info_layout.addWidget(self._info_label)

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

        info_layout.addLayout(grid)

        widget = QtWidgets.QWidget()
        widget.setLayout(info_layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)

        self._info_widget = QtWidgets.QScrollArea()
        self._info_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._info_widget.setWidgetResizable(True)
        self._info_widget.setWidget(widget)
        self._info_widget.verticalScrollBar().valueChanged.connect(
            self.onVertScroll)

        # episode list widgets
        self._all_episodes_layout = QtWidgets.QVBoxLayout()
        self._all_episodes_layout.setContentsMargins(0, 0, 0, 0)
        self._all_episodes_layout.setSpacing(0)

        widget = QtWidgets.QWidget()
        widget.setLayout(self._all_episodes_layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)

        self._list_widget = QtWidgets.QScrollArea()
        self._list_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._list_widget.setWidgetResizable(True)
        self._list_widget.setWidget(widget)
        self._list_widget.verticalScrollBar().valueChanged.connect(
            self.onVertScroll)

        self._stacked_widget = QtWidgets.QStackedWidget()
        self._stacked_widget.addWidget(self._info_widget)
        self._stacked_widget.addWidget(self._list_widget)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(top_layout)
        layout.addWidget(self._stacked_widget)

    @property
    def id(self):
        if self._show is None:
            return None
        else:
            return self._show['id']

    @property
    def active_page(self):
        return self._stacked_widget.currentIndex()

    def setActivePage(self, index):
        self._stacked_widget.setCurrentIndex(index)

    def fill(self, show_id):
        self._show = self._main_window.spotify.show(show_id)

        while self._episodes_layout.count() > 0:
            item = self._episodes_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        img_url = self._show['images'][0]['url']
        self._img = Assets().get(img_url)
        self._img.image_loaded.connect(self.onImageLoaded)

        self._show_title.setText(self._show['name'])
        self._show_author.setText(self._show['publisher'])

        latest_episode = self._show['episodes']['items'][0]
        self._latest_episode.setText(
            ": ".join([latest_episode['name'], latest_episode['description']])
        )

        resume_pt = latest_episode['resume_point']
        if resume_pt['fully_played']:
            text = "\u25B6  Play Again"
        elif resume_pt['resume_position_ms'] == 0:
            text = "\u25B6  Latest Episode"
        else:
            text = "\u25B6  Resume"
        self._play_latest.setText(text)

        self._episode_idx = {}
        for idx, episode in enumerate(self._show['episodes']['items'][0:8]):
            self._episode_idx[episode['id']] = idx
            widget = EpisodeWidget(episode, parent=self._main_window)
            widget.play.connect(self.onPlayFromEpisode)
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
        for lang in self._show['languages']:
            locale = QtCore.QLocale(lang)
            langs.append(QtCore.QLocale.languageToString(locale.language()))
        self._language_info.set(", ".join(langs))
        self._rating_info.set(utils.rating(self._show['explicit']))

        self._play_latest.setEnabled(True)

        # fill episode list
        for idx, episode in enumerate(self._show['episodes']['items']):
            # self._episode_idx[episode['id']] = idx
            widget = EpisodeWidget(episode, parent=self._main_window)
            # widget.play.connect(self.onPlayFromEpisode)
            self._all_episodes_layout.addWidget(widget)

            hline = HLine()
            hline.setStyleSheet(
                "margin-left: 38px; "
                "margin-right: 28px; "
                "color: #444")
            self._all_episodes_layout.addWidget(hline)

    def onBack(self):
        if self._stacked_widget.currentWidget() == self._list_widget:
            self._stacked_widget.setCurrentWidget(self._info_widget)
        else:
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
        LO_VALUE = 80
        HI_VALUE = 100

        if value > LO_VALUE:
            self._show_label.setText(self._show['name'])
            clr2 = QtGui.QColor("#C8C8C8")

            if value < HI_VALUE:
                t = (float(value) - LO_VALUE) / (HI_VALUE - LO_VALUE)
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

    def onPlayLatest(self):
        if self._show is not None:
            episode = self._show['episodes']['items'][0]
            self._main_window.startPlayback([episode['uri']])

    def onPlayFromEpisode(self, episode):
        start_idx = self._episode_idx[episode['id']]
        uris = []
        for ep in self._show['episodes']['items'][start_idx:8]:
            uris.append(ep['uri'])
        self._main_window.startPlayback(uris)

    def onSeeAllEpisodes(self):
        self._stacked_widget.setCurrentWidget(self._list_widget)
