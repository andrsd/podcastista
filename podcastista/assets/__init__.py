import os
import sys
from PyQt5 import QtCore, QtGui, QtNetwork


class NetworkImage(QtCore.QObject):
    """ Image pulled from network """

    image_loaded = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._img = QtGui.QImage()

    def load(self, device, format):
        self._img.load(device, format)
        self.image_loaded.emit()

    def done(self):
        self.image_loaded.emit()

    def scaledToWidth(self, width):
        return self._img.scaledToWidth(width)


class Assets:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.on_new()
        return cls._instance

    def on_new(self):
        if getattr(sys, 'frozen', False):
            path = sys._MEIPASS
        else:
            path = os.path.dirname(__file__)

        self.music_dir = os.path.join(path, 'music')

        icons_dir = os.path.join(path, 'icons')
        self.author_icon = QtGui.QIcon(os.path.join(icons_dir, "author.svg"))
        self.piece_icon = QtGui.QIcon(os.path.join(icons_dir, "vinyl.svg"))
        self.prev_icon = QtGui.QIcon(os.path.join(icons_dir, "prev.svg"))
        self.next_icon = QtGui.QIcon(os.path.join(icons_dir, "next.svg"))
        self.play_icon = QtGui.QIcon(os.path.join(icons_dir, "play.svg"))
        self.pause_icon = QtGui.QIcon(os.path.join(icons_dir, "pause.svg"))

        self.spotify_logo = QtGui.QIcon(os.path.join(
            icons_dir, "spotify-logo.svg"))

        self._img_urls = {}
        self._nam = QtNetwork.QNetworkAccessManager()
        self._nam.finished.connect(self.onNetworkReply)

    def get(self, url):
        if url in self._img_urls:
            img = self._img_urls[url]
            QtCore.QTimer.singleShot(100, img.done)
            return img
        else:
            img = NetworkImage()
            self._img_urls[url] = img

            req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
            reply = self._nam.get(req)

            return img

    def onNetworkReply(self, reply):
        """
        Called when network request was finished
        """
        if reply.url().host() == "localhost":
            # our own requests
            return
        else:
            url = reply.url().toString()
            self._img_urls[url].load(reply, "")
