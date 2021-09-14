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
        # Spotify devices
        self._devices = None
        # active Spotify device Id
        self._active_device_id = None
        self._volume = None
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
              font-weight: bold;
              border-radius: 4px;
              background-color: #808080;
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

        w = QtWidgets.QWidget()
        w.setLayout(self._stacked_layout)

        self._splitter = QtWidgets.QSplitter(self)
        self._splitter.setOrientation(QtCore.Qt.Horizontal)
        self._splitter.setChildrenCollapsible(False)
        self._splitter.addWidget(self._left)
        self._splitter.addWidget(w)

        self.setCentralWidget(self._splitter)

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
            "Next", self.onNext, "Ctrl+Right")
        self._previous = self._controls_menu.addAction(
            "Previous", self.onPrevious, "Ctrl+Left")
        self._controls_menu.addSeparator()
        self._volume_up = self._controls_menu.addAction(
            "Increase Volume", self.onVolumeUp, "Ctrl+Up")
        self._volume_down = self._controls_menu.addAction(
            "Decrease Volume", self.onVolumeDown, "Ctrl+Down")
        self._controls_menu.addSeparator()

        if platform.system() == "Darwin":
            self._window_menu = self._menubar.addMenu("Window")
            self._minimize = self._window_menu.addAction(
                "Minimize", self.onMinimize, "Ctrl+M")
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
        cpb = self._spotify.current_playback()
        if cpb['is_playing'] is True:
            self._spotify.pause_playback(device_id=self._active_device_id)
            self._play_pause.setText("Play")
            self._play_pause_button.setIcon(Assets().play_icon)
        else:
            self._spotify.start_playback(device_id=self._active_device_id)
            self._play_pause.setText("Pause")
            self._play_pause_button.setIcon(Assets().pause_icon)

    def onNext(self):
        """
        Skip to the next track
        """
        pass

    def onPrevious(self):
        """
        Jump to the previous track
        """
        pass

    def onVolumeUp(self):
        """
        Increase volume
        """
        pass

    def onVolumeDown(self):
        """
        Decrease volume
        """
        pass

    def onVolumeChanged(self, value):
        """
        Called when volume was changed
        """
        pass

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
        self._settings.endGroup()

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

        # get active playback device and save its state
        devs = self._spotify.devices()
        self._devices = []
        for d in devs['devices']:
            self._devices.append(d)
            if d['is_active'] is True:
                self._active_device_id = d['id']
                self._volume = d['volume_percent']

        self._shows_tab.fill()
        self._listen_now_tab.fill()

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

    def onViewEpisodes(self):
        self._stacked_layout.setCurrentWidget(self._episodes_tab)

    def onViewShows(self):
        self._stacked_layout.setCurrentWidget(self._shows_tab)

    def viewShow(self, show_id):
        """
        Display "Show details"

        @param show_id ID of the show from spotify
        """
        self._history.append(self._stacked_layout.currentWidget())
        self._show.setShow(show_id)
        self._stacked_layout.setCurrentWidget(self._show)

    def onBack(self):
        """
        Go back
        """
        w = self._history.pop()
        self._stacked_layout.setCurrentWidget(w)

    def followShow(self, show_id):
        # TODO
        pass

    def viewEpisode(self, episode):
        """
        Display "Episode details"

        @param episode Episode data object from spotify
        """
        self._history.append(self._stacked_layout.currentWidget())
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
