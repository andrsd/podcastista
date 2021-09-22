"""
MainWindow.py
"""

import sys
import random
import platform
from PyQt5 import QtWidgets, QtCore, QtNetwork, QtGui
from podcastista import server
from podcastista.assets import Assets
from podcastista.AboutDialog import AboutDialog
from podcastista.ListenNowTab import ListenNowTab
from podcastista.EpisodesListTab import EpisodesListTab
from podcastista.ShowsTab import ShowsTab
from podcastista.SearchTab import SearchTab
from podcastista.ShowDetails import ShowDetails
from podcastista.EpisodeDetails import EpisodeDetails
from podcastista.Player import Player


WINDOW_TITLE = "Podcastista"


class MainWindow(QtWidgets.QMainWindow):
    """
    Main window
    """

    ALBUM_IMAGE_WD = 128
    ALBUM_IMAGE_HT = 128

    VOLUME_PAGE_STEP = 5
    VOLUME_MINIMUM = 0
    VOLUME_MAXIMUM = 100

    # delay in milliseconds for updating player status (assumes good connection
    # to Spotify)
    UPDATE_DELAY_MS = 500

    LISTEN_NOW_ID = 1
    SHOWS_ID = 2
    LATEST_EPISODES_ID = 3

    def __init__(self):
        super().__init__()
        random.seed()
        # Spotify object
        self._spotify = None
        # my Spotify profile
        self._me = None
        self._settings = QtCore.QSettings()
        self._about_dlg = None
        self._window_menu = None

        self._splitter = None
        self._episodes_tab = None
        self._shows_tab = None
        self._search_tab = None
        self._show = None
        self._episode_detail = None

        server.signaler.connectToSpotify.connect(self.setupSpotify)

        self._nam = QtNetwork.QNetworkAccessManager()
        self._nam.finished.connect(self.onNetworkReply)

        self._history = []

        self.setupWidgets()
        self.readSettings()
        self.setWindowTitle(WINDOW_TITLE)
        self.setupMenuBar()
        self.updateMenuBar()

    def setupWidgets(self):
        """
        Setup widgets
        """
        self._listen_now_tab = ListenNowTab(self)
        self._episodes_tab = EpisodesListTab(self)
        self._shows_tab = ShowsTab(self)
        self._search_tab = SearchTab(self)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.setSpacing(4)

        search_ss = """
            QLineEdit {
              background-color: #444;
              border-radius: 4px;
            }
            QLineEdit:focus {
              border-radius: 4px;
              background-color: #555;
              border: 3px solid #006040;
            }"""
        self._search_box = QtWidgets.QLineEdit()
        self._search_box.setPlaceholderText("Search")
        self._search_box.setClearButtonEnabled(True)
        self._search_box.setFixedHeight(25)
        self._search_box.setStyleSheet(search_ss)
        self._search_box.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self._search_box.installEventFilter(self)
        self._search_box.returnPressed.connect(self.onSearch)
        self._search_box.textChanged.connect(self.onSearchTextChanged)
        left_layout.addWidget(self._search_box)

        left_layout.addSpacing(20)

        item_ss = """
            QPushButton {
              text-align: left;
              padding: 4 8 4 8;
            }
            QPushButton:checked {
              border-radius: 4px;
              background-color: #444;
              border: none;
            }"""

        self._left_listen_now = QtWidgets.QPushButton("Listen Now")
        self._left_listen_now.setFlat(True)
        self._left_listen_now.setCheckable(True)
        self._left_listen_now.setStyleSheet(item_ss)
        left_layout.addWidget(self._left_listen_now)

        self._left_shows = QtWidgets.QPushButton("Shows")
        self._left_shows.setFlat(True)
        self._left_shows.setCheckable(True)
        self._left_shows.setStyleSheet(item_ss)
        left_layout.addWidget(self._left_shows)

        self._left_latest_episodes = QtWidgets.QPushButton("Latest Episodes")
        self._left_latest_episodes.setFlat(True)
        self._left_latest_episodes.setCheckable(True)
        self._left_latest_episodes.setStyleSheet(item_ss)
        left_layout.addWidget(self._left_latest_episodes)

        self._left_group = QtWidgets.QButtonGroup()
        self._left_group.setExclusive(True)
        self._left_group.addButton(self._left_listen_now, self.LISTEN_NOW_ID)
        self._left_group.addButton(self._left_shows, self.SHOWS_ID)
        self._left_group.addButton(self._left_latest_episodes,
                                   self.LATEST_EPISODES_ID)

        self._left_group.buttonClicked.connect(self.onLeftGroupClicked)

        left_layout.addStretch()

        powered_by_layout = QtWidgets.QHBoxLayout()

        powered_by_layout.addStretch()

        powered_by_label = QtWidgets.QLabel("Powered by")
        powered_by_layout.addWidget(powered_by_label, 0, QtCore.Qt.AlignRight)

        spotify_logo = QtWidgets.QLabel()
        spotify_logo.setPixmap(Assets().spotify_logo.pixmap(80, 24))
        powered_by_layout.addWidget(spotify_logo, 0, QtCore.Qt.AlignRight)

        left_layout.addLayout(powered_by_layout)

        self._left = QtWidgets.QWidget()
        self._left.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                 QtWidgets.QSizePolicy.Expanding)
        self._left.setMinimumWidth(200)
        self._left.setMaximumWidth(250)
        self._left.setStyleSheet("background-color: #222")

        self._left.setLayout(left_layout)

        #
        self._show = ShowDetails(self)
        self._episode_detail = EpisodeDetails(self)

        self._stacked_layout = QtWidgets.QStackedLayout()
        self._stacked_layout.addWidget(self._search_tab)
        self._stacked_layout.addWidget(self._listen_now_tab)
        self._stacked_layout.addWidget(self._episodes_tab)
        self._stacked_layout.addWidget(self._shows_tab)
        self._stacked_layout.addWidget(self._show)
        self._stacked_layout.addWidget(self._episode_detail)

        self._right = QtWidgets.QWidget()
        self._right.setLayout(self._stacked_layout)

        self._splitter = QtWidgets.QSplitter(self)
        self._splitter.setOrientation(QtCore.Qt.Horizontal)
        self._splitter.setChildrenCollapsible(False)
        self._splitter.addWidget(self._left)
        self._splitter.addWidget(self._right)

        self._player = Player(self)
        self._player.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Fixed)
        self._player.setFixedHeight(96)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._splitter)
        layout.addWidget(self._player)

        w = QtWidgets.QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.setMinimumWidth(780)
        self.setMinimumHeight(480)

        self._shows_tab.shows_loaded.connect(self._episodes_tab.fill)

    def setupMenuBar(self):
        """
        Setup menu bar
        """
        self._menubar = QtWidgets.QMenuBar(self)

        self._file_menu = self._menubar.addMenu("File")

        # The "About" item is fine here, since we assume Mac and that will
        # place the item into  different submenu but this will need to be fixed
        # for linux and windows
        self._file_menu.addSeparator()
        self._about_box_action = self._file_menu.addAction(
            "About...", self.onAbout)

        self._view_menu = self._menubar.addMenu("View")
        self._view_episodes = self._view_menu.addAction(
            "Episodes", self.onViewEpisodes, "Ctrl+1")
        self._view_shows = self._view_menu.addAction(
            "Shows", self.onViewShows, "Ctrl+2")

        self._controls_menu = self._menubar.addMenu("Controls")
        self._play_pause = self._controls_menu.addAction(
            "Play", self.onPlayPause, "Space")
        self._next = self._controls_menu.addAction(
            "Next", self._player.onNext, "Ctrl+Right")
        self._previous = self._controls_menu.addAction(
            "Previous", self._player.onPrev, "Ctrl+Left")
        self._controls_menu.addSeparator()
        self._volume_up = self._controls_menu.addAction(
            "Increase Volume", self._player.onVolumeUp, "Ctrl+Up")
        self._volume_down = self._controls_menu.addAction(
            "Decrease Volume", self._player.onVolumeDown, "Ctrl+Down")
        self._controls_menu.addSeparator()

        if platform.system() == "Darwin":
            self._window_menu = self._menubar.addMenu("Window")
            self._minimize = self._window_menu.addAction(
                "Minimize", self.onMinimize, "Ctrl+M")
            self._zoom = self._window_menu.addAction(
                "Zoom", self.onZoom)
            self._window_menu.addSeparator()
            self._bring_all_to_front = self._window_menu.addAction(
                "Bring All to Front", self.onBringAllToFront)

        self.setMenuBar(self._menubar)

    def updateMenuBar(self):
        """
        Update menu bar
        """
        pass

    def onPlayPause(self):
        """
        Start/Pause the playback
        """
        if self._player.cpb['is_playing'] is True:
            self._play_pause.setText("Play")
        else:
            self._play_pause.setText("Pause")
        self._player.onPlayPause()

    def onAbout(self):
        """
        Called when FileAbout action is triggered
        """
        if self._about_dlg is None:
            self._about_dlg = AboutDialog(self)
        self._about_dlg.show()

    def onMinimize(self):
        """
        Called when WindowMinimize is triggered
        """
        self.showMinimized()

    def onZoom(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def onBringAllToFront(self):
        """
        Called when WindowBringAllToFront is triggered
        """
        self.showNormal()

    def onShowMainWindow(self):
        """
        Called when show main window is triggered
        """
        self.showNormal()
        self.activateWindow()
        self.raise_()
        self.updateMenuBar()

    def event(self, event):
        """
        Event override
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            self.updateMenuBar()
        return super().event(event)

    def resizeEvent(self, event):
        """
        Resize event
        """
        pass

    def closeEvent(self, event):
        """
        Called when EventClose is received
        """
        self.writeSettings()
        event.accept()
        if platform.system() != "Darwin":
            sys.exit()

    def writeSettings(self):
        """
        Write settings
        """
        self._settings.beginGroup("MainWindow")
        self._settings.setValue("geometry", self.saveGeometry())
        self._settings.setValue("splitter", self._splitter.saveState())
        active_page = self._stacked_layout.currentIndex()
        self._settings.setValue("active_page", active_page)
        self._settings.setValue("active_show_id", self._show.id)
        self._settings.setValue("active_episode_id", self._episode_detail.id)
        self._settings.setValue("history", self._history)
        self._settings.endGroup()

        self._settings.setValue("device_id", self._player.active_device_id)

    def readSettings(self):
        """
        Read settings
        """
        self._settings.beginGroup("MainWindow")
        geom = self._settings.value("geometry")
        if geom is None:
            # screen_rc = QtWidgets.QApplication.desktop().screenGeometry()
            # wnd_wd = 600
            # wnd_ht = self.ALBUM_IMAGE_HT + 24
            # self.setGeometry(QtCore.QRect(
            #     screen_rc.width() - wnd_wd - 10, 10,
            #     wnd_wd, wnd_ht))
            pass
        else:
            self.restoreGeometry(geom)
        state = self._settings.value("splitter")
        if state is not None:
            self._splitter.restoreState(state)
        active_page = self._settings.value("active_page", 0)
        if active_page != -1:
            self._stacked_layout.setCurrentIndex(active_page)
        self._history = self._settings.value("history", [])
        self._settings.endGroup()

    @property
    def spotify(self):
        return self._spotify

    def connectToSpotify(self):
        """
        Connect to Spotify via our local HTTP server
        """
        spotify_req = QtNetwork.QNetworkRequest(
            QtCore.QUrl("http://localhost:{}".format(server.port)))
        self._nam.get(spotify_req)

    def setupSpotify(self, spotify):
        """
        Link Spotify information to our internal data
        """
        self._spotify = spotify
        if spotify is None:
            return

        self._me = self._spotify.me()

        self._player.update()
        self.loadData()
        self._restoreState()

    def _restoreState(self):
        act_tab = None
        self._settings.beginGroup("MainWindow")
        if self._stacked_layout.currentWidget() == self._listen_now_tab:
            act_tab = self._listen_now_tab
        elif self._stacked_layout.currentWidget() == self._shows_tab:
            act_tab = self._shows_tab
        elif self._stacked_layout.currentWidget() == self._episodes_tab:
            act_tab = self._episodes_tab
        elif self._stacked_layout.currentWidget() == self._show:
            show_id = self._settings.value("active_show_id")
            if show_id is not None:
                self._show.fill(show_id)
            act_tab = self._stacked_layout.widget(self._history[0])
        elif self._stacked_layout.currentWidget() == self._episode_detail:
            episode_id = self._settings.value("active_episode_id")
            if episode_id is not None:
                episode = self._spotify.episode(episode_id)
                self._episode_detail.fill(episode)
            act_tab = self._stacked_layout.widget(self._history[0])
        self._settings.endGroup()

        if act_tab == self._listen_now_tab:
            self._left_listen_now.setChecked(True)
            self._left_listen_now.setFocus(QtCore.Qt.OtherFocusReason)
        elif act_tab == self._shows_tab:
            self._left_shows.setChecked(True)
            self._left_shows.setFocus(QtCore.Qt.OtherFocusReason)
        elif act_tab == self._episodes_tab:
            self._left_latest_episodes.setChecked(True)
            self._left_latest_episodes.setFocus(QtCore.Qt.OtherFocusReason)

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
            scaled_img = img.scaledToWidth(self.ALBUM_IMAGE_WD)
            pixmap = QtGui.QPixmap.fromImage(scaled_img)
            self._image.setPixmap(pixmap)

    def reportUnknownDeviceId(self):
        """
        Show message box reporting unknown device ID
        """
        mb = QtWidgets.QMessageBox(self)
        mb.setIcon(QtWidgets.QMessageBox.Critical)
        mb.setWindowTitle("Error")
        mb.addButton(QtWidgets.QMessageBox.Ok)
        mb.setText("Device ID unknown")
        mb.setInformativeText(
            "Try restarting Spotify and then this application.")
        horizontalSpacer = QtWidgets.QSpacerItem(
            400, 0,
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout = mb.layout()
        layout.addItem(
            horizontalSpacer, layout.rowCount(), 0, 1, layout.columnCount())
        mb.exec()

    def clearData(self):
        self._shows_tab.clear()
        self._episodes_tab.clear()
        self._listen_now_tab.clear()

    def loadData(self):
        self._shows_tab.fill()
        self._listen_now_tab.fill()

    def onViewEpisodes(self):
        self._stacked_layout.setCurrentWidget(self._episodes_tab)

    def onViewShows(self):
        self._stacked_layout.setCurrentWidget(self._shows_tab)

    def viewShow(self, show_id):
        """
        Display "Show details"

        @param show_id ID of the show from spotify
        """
        self._history.append(self._stacked_layout.currentIndex())
        self._show.fill(show_id)
        self._stacked_layout.setCurrentWidget(self._show)

    def onBack(self):
        """
        Go back
        """
        idx = self._history.pop()
        self._stacked_layout.setCurrentIndex(idx)

    def followShow(self, show_id):
        self.spotify.current_user_saved_shows_add([show_id])
        self.clearData()
        self.loadData()

    def unfollowShow(self, show_id):
        self.spotify.current_user_saved_shows_delete([show_id])
        self.clearData()
        self.loadData()

    def viewEpisode(self, episode):
        """
        Display "Episode details"

        @param episode Episode data object from spotify
        """
        self._history.append(self._stacked_layout.currentIndex())
        self._episode_detail.fill(episode)
        self._stacked_layout.setCurrentWidget(self._episode_detail)

    def onSearch(self):
        self._stacked_layout.setCurrentWidget(self._search_tab)

        self._search_tab.clear()
        text = self._search_box.text()
        self._search_tab.search(text)

    def onSearchTextChanged(self, text):
        if len(text) == 0:
            self._search_tab.clear()

    def onLeftGroupClicked(self, button):
        id = self._left_group.id(button)
        button.setFocus()
        if id == self.LISTEN_NOW_ID:
            self._stacked_layout.setCurrentWidget(self._listen_now_tab)
        elif id == self.SHOWS_ID:
            self._stacked_layout.setCurrentWidget(self._shows_tab)
        elif id == self.LATEST_EPISODES_ID:
            self._stacked_layout.setCurrentWidget(self._episodes_tab)
        self._history = []

    def startPlayback(self, uris):
        self.spotify.start_playback(
            device_id=self._player.active_device_id,
            uris=uris)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.FocusOut and
                source is self._search_box):
            self.onSearchFocusOut()
        elif (event.type() == QtCore.QEvent.FocusIn and
                source is self._search_box):
            self.onSearchFocusIn()
        return super(QtWidgets.QMainWindow, self).eventFilter(source, event)

    def onSearchFocusIn(self):
        self._stacked_layout.setCurrentWidget(self._search_tab)

    def onSearchFocusOut(self):
        pass
