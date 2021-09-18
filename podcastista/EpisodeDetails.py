from PyQt5 import QtWidgets, QtCore, QtGui
from podcastista.assets import Assets
from podcastista.HLine import HLine
from podcastista.BackButton import BackButton
from podcastista.SubsectionTitle import SubsectionTitle
from podcastista.InfoLabel import InfoLabel
from podcastista import utils


class EpisodeDetails(QtWidgets.QWidget):
    """
    Widget on main window with show details
    """

    ARTWORK_WD = 200
    ARTWORK_HT = 200
    LINE_HT = 16

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
        self._episode = None
        self._follow_button = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setContentsMargins(4, 4, 4, 4)

        self._back = BackButton()
        self._back.clicked.connect(self.onBack)
        top_layout.addWidget(self._back)

        self._episode_label = QtWidgets.QLabel()
        self._episode_label.setAlignment(QtCore.Qt.AlignCenter)
        self._episode_label.setStyleSheet("""
            font-weight: bold;
            """)
        top_layout.addWidget(self._episode_label)

        layout.addLayout(top_layout)

        scroll_layout = QtWidgets.QVBoxLayout()
        scroll_layout.setSpacing(8)
        scroll_layout.setContentsMargins(16, 0, 16, 16)

        banner_h_layout = QtWidgets.QHBoxLayout()
        banner_h_layout.setContentsMargins(16, 16, 16, 16)
        banner_h_layout.setSpacing(40)

        self._artwork = QtWidgets.QLabel()
        self._artwork.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._artwork.setFixedSize(self.ARTWORK_WD, self.ARTWORK_HT)
        banner_h_layout.addWidget(self._artwork)

        banner_right_layout = QtWidgets.QVBoxLayout()
        banner_right_layout.setSpacing(2)

        banner_right_layout.addSpacing(25)

        self._date = QtWidgets.QLabel()
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
        banner_right_layout.addWidget(self._date)

        self._title = QtWidgets.QLabel()
        self._title.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self._title.setWordWrap(True)
        self._title.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        font = self._title.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSize() * 2)
        self._title.setFont(font)
        banner_right_layout.addWidget(self._title)

        banner_right_layout.addSpacing(10)

        self._play = QtWidgets.QPushButton("\u25B6  Play")
        css = """
            border-radius: 4px;
            background-color: #307BF6;
            border: none;
            font-weight: bold;
            font-size: 14px;
            """
        self._play.setFlat(True)
        self._play.setStyleSheet(css)
        self._play.setFixedWidth(150)
        self._play.setFixedHeight(28)
        self._play.setContentsMargins(0, 0, 0, 0)
        self._play.setEnabled(False)
        self._play.clicked.connect(self.onPlay)
        banner_right_layout.addWidget(self._play)

        banner_h_layout.addLayout(banner_right_layout)

        banner = QtWidgets.QWidget()
        banner.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        banner.setLayout(banner_h_layout)
        scroll_layout.addWidget(banner)

        hline = HLine()
        hline.setStyleSheet(
            "margin-left: 16px; "
            "margin-right: 16px; "
            "color: #444")
        scroll_layout.addWidget(hline)

        self._description = QtWidgets.QLabel()
        self._description.setWordWrap(True)
        self._description.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._description.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        font = self._description.font()
        font.setPointSizeF(font.pointSize() * 1.15)
        self._description.setFont(font)
        self._description.setContentsMargins(16, 20, 240, 20)
        scroll_layout.addWidget(self._description)

        hline = HLine()
        hline.setStyleSheet(
            "margin-left: 16px; "
            "margin-right: 16px; "
            "color: #444")
        scroll_layout.addWidget(hline)

        scroll_layout.addSpacing(8)

        self._info_label = SubsectionTitle("Information")
        self._info_label.setStyleSheet("margin-left: 12px")
        scroll_layout.addWidget(self._info_label)

        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(8, 0, 8, 0)

        self._length_info = InfoLabel("Length")
        grid.addWidget(self._length_info, 0, 0)

        self._pub_date_info = InfoLabel("Published")
        grid.addWidget(self._pub_date_info, 0, 1)

        self._language_info = InfoLabel("Language")
        grid.addWidget(self._language_info, 1, 0)

        self._rating_info = InfoLabel("Rating")
        grid.addWidget(self._rating_info, 1, 1)

        scroll_layout.addLayout(grid)

        scroll_layout.addStretch()

        widget = QtWidgets.QWidget()
        widget.setLayout(scroll_layout)
        widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)
        scroll_area.verticalScrollBar().valueChanged.connect(self.onVertScroll)

        layout.addWidget(scroll_area)

    @property
    def id(self):
        if self._episode is None:
            return None
        else:
            return self._episode['id']

    def fill(self, episode):
        self._episode = episode

        images = self._episode['images']
        img_url = None
        for img in images:
            if (img['height'] >= self.ARTWORK_HT and img['height'] <= 300):
                img_url = img['url']
        self._img = Assets().get(img_url)
        self._img.image_loaded.connect(self.onImageLoaded)

        time = utils.msToTime(self._episode['duration_ms'])
        date = utils.dateToStr(self._episode['release_date'])
        self._date.setText('   |   '.join([date, time]))

        self._title.setText(self._episode['name'])

        self._description.setText(self._episode['description'])

        self._length_info.set(time)
        self._pub_date_info.set(utils.longDate(self._episode['release_date']))
        locale = QtCore.QLocale(self._episode['language'])
        lang = QtCore.QLocale.languageToString(locale.language())
        self._language_info.set(lang)
        self._rating_info.set(utils.rating(self._episode['explicit']))

        self._play.setEnabled(True)

    def onBack(self):
        self._main_window.onBack()

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._artwork.setPixmap(pixmap)

    def onVertScroll(self, value):
        LO_VALUE = 90
        HI_VALUE = 110

        if value > LO_VALUE:
            self._episode_label.setText(self._episode['name'])
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
            self._episode_label.setStyleSheet(qss)
        else:
            self._episode_label.setText("")

    def onPlay(self):
        if self._episode is not None:
            self._main_window.startPlayback([self._episode['uri']])
