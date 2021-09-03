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

if platform.system() == "Darwin":
    WINDOW_TITLE = "Player"
else:
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

        server.signaler.connectToSpotify.connect(self.setupSpotify)

        self._nam = QtNetwork.QNetworkAccessManager()
        self._nam.finished.connect(self.onNetworkReply)

        self.readSettings()
        self.setWindowTitle(WINDOW_TITLE)
        self.setupWidgets()
        self.setupMenuBar()
        self.updateMenuBar()

    def setupWidgets(self):
        """
        Setup widgets
        """
        w = QtWidgets.QWidget(self)
        w.setContentsMargins(0, 0, 0, 0)

        # w.setLayout(h_layout)
        self.setCentralWidget(w)

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
        self._settings.endGroup()

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