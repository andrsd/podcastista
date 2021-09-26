from PyQt5 import QtWidgets, QtCore, QtGui
from podcastista.assets import Assets
from podcastista import utils
from podcastista.ClickableLabel import ClickableLabel
from podcastista.EpisodePlayButton import EpisodePlayButton
from podcastista.EpisodeContextMenu import EpisodeContextMenu


class EpisodeWidget(QtWidgets.QWidget):

    play = QtCore.pyqtSignal(object)

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
        self._layout.setContentsMargins(0, 16, 16, 16)
        self._layout.setSpacing(0)

        self._played = False
        if ('resume_point' in episode and
                episode['resume_point']['fully_played']):
            self._played = True

        if artwork:
            self._layout.addSpacing(20)

            self._artwork = QtWidgets.QLabel()
            self._artwork.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self._artwork.setFixedSize(self.ARTWORK_WD, self.ARTWORK_HT)
            self._artwork.setStyleSheet("border: 1px solid #fff")

            play_button_layout = QtWidgets.QBoxLayout(
                QtWidgets.QBoxLayout.LeftToRight)

            self._play = EpisodePlayButton(
                Assets().ep_play_normal_icon,
                Assets().ep_play_selected_icon
            )
            self._play.setSize(QtCore.QSize(40, 40))
            self._play.setVisible(False)
            self._play.clicked.connect(self.onPlay)

            play_button_layout.addWidget(self._play, 0, QtCore.Qt.AlignCenter)
            self._artwork.setLayout(play_button_layout)

            self._layout.addWidget(self._artwork)

            img_url = self._episode['images'][0]['url']
            self._img = Assets().get(img_url)
            self._img.image_loaded.connect(self.onImageLoaded)

            self._layout.addSpacing(8)
        else:
            play_button_layout = QtWidgets.QVBoxLayout()

            play_button_layout.addSpacing(self.LINE_HT + 2)

            self._play = QtWidgets.QPushButton("\u25B6")
            css = """
                QPushButton {
                    color: #282828;
                }
                QPushButton:hover {
                    color: #307BF6;
                }
                """
            self._play.setFlat(True)
            self._play.setStyleSheet(css)
            self._play.setFixedWidth(38)
            self._play.setFixedHeight(28)
            self._play.setContentsMargins(0, 0, 0, 0)
            font = self._play.font()
            font.setPointSizeF(font.pointSize() * 1.3)
            self._play.setFont(font)
            self._play.setVisible(False)
            self._play.clicked.connect(self.onPlay)
            play_button_layout.addWidget(self._play)

            spacer = QtWidgets.QSpacerItem(
                38, 0,
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            play_button_layout.addItem(spacer)

            self._layout.addLayout(play_button_layout)

            self._artwork = None
            self._img = None

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.setSpacing(6)

        self._date = QtWidgets.QLabel(
            utils.dateToStr(self._episode['release_date']))
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

        self._title = ClickableLabel(self._episode['name'])
        self._title.setWordWrap(True)
        self._title.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._title.setMaximumHeight(2 * self.LINE_HT + 6)
        font = self._title.font()
        font.setPointSizeF(font.pointSize() * 1.2)
        if (episode['resume_point']['resume_position_ms'] == 0 and
                not episode['resume_point']['fully_played']):
            font.setBold(True)
        self._title.setFont(font)
        self._title.clicked.connect(self.onTitleClicked)
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

        self._layout.addSpacing(20)

        duration_layout = QtWidgets.QVBoxLayout()

        duration_layout.addStretch()

        resume_pt = episode['resume_point']
        progress_visible = False
        if self._played:
            time = "Played"
        elif resume_pt['resume_position_ms'] == 0:
            time = utils.msToTime(self._episode['duration_ms'])
        else:
            left_ms = episode['duration_ms'] - resume_pt['resume_position_ms']
            time = utils.msToTime(left_ms) + " left"
            progress_visible = True

        self._duration = QtWidgets.QLabel(time)
        self._duration.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self._duration.setFixedWidth(self.TIME_WD)
        self._duration.setAlignment(QtCore.Qt.AlignCenter)

        duration_layout.addWidget(self._duration)

        self._duration_progress = QtWidgets.QProgressBar(self)
        self._duration_progress.setVisible(progress_visible)
        self._duration_progress.setRange(0, episode['duration_ms'])
        self._duration_progress.setValue(resume_pt['resume_position_ms'])
        self._duration_progress.setTextVisible(False)
        self._duration_progress.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        duration_layout.addWidget(self._duration_progress)

        duration_layout.addStretch()

        self._layout.addLayout(duration_layout)

        self._layout.addSpacing(20)

        actions_layout = QtWidgets.QHBoxLayout()

        self._dots_menu = EpisodeContextMenu(self._main_window, self._episode)
        self._dots_btn = QtWidgets.QPushButton("...")
        self._dots_btn.setStyleSheet("""
            QPushButton {
                border:none;
            }
            QPushButton::menu-indicator {
                image: none;
            }
            """)
        self._dots_btn.setFlat(True)
        self._dots_btn.setMenu(self._dots_menu)
        actions_layout.addWidget(self._dots_btn)
        self._layout.addLayout(actions_layout)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            EpisodeWidget { background-color: #282828 }
            EpisodeWidget:hover { background-color: #363636 }
            """)

    def enterEvent(self, event):
        self._play.setVisible(True)

    def leaveEvent(self, event):
        self._play.setVisible(False)

    def onClicked(self):
        self._main_window.viewEpisode(self._episode)

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._artwork.setPixmap(pixmap)

    def onPlay(self):
        self.play.emit(self._episode)

    def onTitleClicked(self):
        self.onClicked()
