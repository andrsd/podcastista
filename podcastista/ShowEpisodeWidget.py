from PyQt5 import QtWidgets, QtGui, QtCore
from podcastista.assets import Assets
from podcastista import utils
from podcastista.ClickableLabel import ClickableLabel
from podcastista.EpisodePlayButton import EpisodePlayButton
from podcastista.EpisodeContextMenu import EpisodeContextMenu


class ShowEpisodeWidget(QtWidgets.QWidget):

    ARTWORK_WD = 220
    ARTWORK_HT = 220
    LINE_HT = 16
    SPACE = 4

    def __init__(self, show, parent=None):
        super().__init__(parent)
        self._show = show
        self._episode = self._show['episodes'][0]
        self._main_window = parent

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(6)

        self._stacked_artwork_layout = QtWidgets.QStackedLayout()
        self._stacked_artwork_layout.setStackingMode(
            QtWidgets.QStackedLayout.StackAll)

        self._artwork = QtWidgets.QLabel(self)
        self._artwork.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._artwork.setFixedSize(self.ARTWORK_WD, self.ARTWORK_HT)

        img_url = self._show['images'][0]['url']
        self._img = Assets().get(img_url)
        self._img.image_loaded.connect(self.onImageLoaded)

        self._stacked_artwork_layout.addWidget(self._artwork)

        # controls part
        self._controls = QtWidgets.QStackedWidget()

        buttons_layout = QtWidgets.QHBoxLayout()

        self._play_btn = EpisodePlayButton(
            Assets().ep_play_normal_icon,
            Assets().ep_play_selected_icon
        )
        self._play_btn.clicked.connect(self.onPlay)
        buttons_layout.addWidget(
            self._play_btn,
            0,
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        buttons_layout.addStretch()

        self._dots_menu = EpisodeContextMenu(self._main_window, self._episode)
        self._dots_btn = EpisodePlayButton(
            Assets().ep_dots_normal_icon,
            Assets().ep_dots_selected_icon
        )
        self._dots_btn.setStyleSheet("""
            QPushButton {
                border:none;
            }
            QPushButton::menu-indicator {
                image: none;
            }
            """)
        buttons_layout.addWidget(
            self._dots_btn,
            0,
            QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self._dots_btn.setMenu(self._dots_menu)

        self._buttons = QtWidgets.QWidget()
        self._buttons.setLayout(buttons_layout)

        self._controls.addWidget(self._buttons)

        # progress part
        progress_layout = QtWidgets.QHBoxLayout()

        self._progress_bar = QtWidgets.QProgressBar(self)
        progress_layout.addWidget(
            self._progress_bar, 0, QtCore.Qt.AlignBottom)

        self._progress = QtWidgets.QWidget()
        self._progress.setLayout(progress_layout)

        self._controls.addWidget(self._progress)
        self._controls.setCurrentWidget(self._progress)

        self._stacked_artwork_layout.addWidget(self._controls)

        self._layout.addLayout(self._stacked_artwork_layout)

        self._layout.addSpacing(8)

        resume_pt = self._episode['resume_point']
        self._progress_bar.setRange(0, self._episode['duration_ms'])
        self._progress_bar.setValue(resume_pt['resume_position_ms'])

        if resume_pt['resume_position_ms'] == 0:
            self._progress_bar.setVisible(False)
        else:
            self._progress_bar.setVisible(True)

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
        if resume_pt['resume_position_ms'] == 0:
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
        self._title.clicked.connect(self.onShowNameClicked)
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

    def enterEvent(self, event):
        self._controls.setCurrentWidget(self._buttons)
        self._play_btn.setVisible(True)

    def leaveEvent(self, event):
        self._controls.setCurrentWidget(self._progress)
        self._play_btn.setVisible(False)

    def onClicked(self):
        self.onShowNameClicked()

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._artwork.setPixmap(pixmap)

    def onEpisodeNameClicked(self):
        self._main_window.viewEpisode(self._episode)

    def onShowNameClicked(self):
        self._main_window.viewShow(self._show['id'])

    def onPlay(self):
        self._main_window.startPlayback([self._episode['uri']])
