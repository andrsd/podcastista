from PyQt5 import QtWidgets, QtGui


class EpisodeContextMenu(QtWidgets.QMenu):

    def __init__(self, parent, episode):
        super().__init__()
        self._main_window = parent
        self._episode = episode

        if ('external_urls' in self._episode and
                'spotify' in self._episode['external_urls']):
            self._uri = self._episode['external_urls']['spotify']
        else:
            self._uri = None

        self._add_to_queue_action = self.addAction("Add to queue")
        self._add_to_queue_action.triggered.connect(self.onAddToQueue)
        self._copy_link_action = self.addAction("Copy link")
        self._copy_link_action.triggered.connect(self.onCopyLink)

    def onAddToQueue(self):
        if self._uri is not None:
            self._main_window.addToQueue(self._uri)

    def onCopyLink(self):
        if self._uri is not None:
            clipboard = QtGui.QGuiApplication.clipboard()
            clipboard.setText(self._uri)
