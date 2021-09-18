from PyQt5 import QtWidgets, QtCore, QtGui
from podcastista.assets import Assets
from podcastista import utils


class Player(QtWidgets.QLabel):

    ARTWORK_WD = 64
    ARTWORK_HT = 64

    UPDATE_MS = 1000

    VOLUME_MINIMUM = 0
    VOLUME_MAXIMUM = 100
    VOLUME_PAGE_STEP = 6

    def __init__(self, parent):
        super().__init__(parent)
        self._main_window = parent
        # convenience
        self._spotify = None
        # active Spotify device Id
        self._active_device_id = None
        # Spotify devices
        self._devices = None
        self._img = None
        self._cpb = None
        self._muted = None

        self.setStyleSheet("""
            background-color: #181818;
            """)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        curr_playing = QtWidgets.QWidget()
        curr_playing.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Expanding)
        curr_playing.setFixedWidth(300)

        cp_layout = QtWidgets.QHBoxLayout()
        self._artwork = QtWidgets.QLabel()
        self._artwork.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._artwork.setFixedSize(self.ARTWORK_WD, self.ARTWORK_HT)
        cp_layout.addWidget(self._artwork)

        label_layout = QtWidgets.QVBoxLayout()
        label_layout.setSpacing(1)

        label_layout.addStretch()

        self._episode_name = QtWidgets.QLabel()
        self._episode_name.setStyleSheet("""
            font-weight: bold;
            font-size: 12px;
            """)
        label_layout.addWidget(self._episode_name)

        self._show_name = QtWidgets.QLabel()
        self._show_name.setStyleSheet("""
            font-size: 11px;
            """)
        label_layout.addWidget(self._show_name)

        label_layout.addStretch()

        cp_layout.addLayout(label_layout)

        curr_playing.setLayout(cp_layout)
        layout.addWidget(curr_playing, 0, QtCore.Qt.AlignLeft)

        layout.addSpacing(30)

        ctrl_layout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()

        self._prev_button = QtWidgets.QPushButton()
        self._prev_button.setIcon(Assets().prev_icon)
        self._prev_button.setIconSize(QtCore.QSize(32, 32))
        self._prev_button.setFixedSize(QtCore.QSize(32, 32))
        self._prev_button.setStyleSheet("QPushButton {border:none}")
        self._prev_button.setEnabled(False)
        self._prev_button.clicked.connect(self.onPrev)
        button_layout.addWidget(self._prev_button)

        self._play_pause_button = QtWidgets.QPushButton()
        self._play_pause_button.setIcon(Assets().play_icon)
        self._play_pause_button.setIconSize(QtCore.QSize(32, 32))
        self._play_pause_button.setFixedSize(QtCore.QSize(32, 32))
        self._play_pause_button.setStyleSheet("QPushButton {border:none}")
        self._play_pause_button.setEnabled(False)
        self._play_pause_button.clicked.connect(self.onPlayPause)
        button_layout.addWidget(self._play_pause_button)

        self._next_button = QtWidgets.QPushButton()
        self._next_button.setIcon(Assets().next_icon)
        self._next_button.setIconSize(QtCore.QSize(32, 32))
        self._next_button.setFixedSize(QtCore.QSize(32, 32))
        self._next_button.setStyleSheet("QPushButton {border:none}")
        self._next_button.setEnabled(False)
        self._prev_button.clicked.connect(self.onNext)
        button_layout.addWidget(self._next_button)

        button_layout.addStretch()

        ctrl_layout.addLayout(button_layout)
        ctrl_layout.setContentsMargins(0, 0, 0, 0)

        progress_layout = QtWidgets.QHBoxLayout()

        self._curr_time = QtWidgets.QLabel()
        self._curr_time.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        progress_layout.addWidget(self._curr_time)

        self._progress = QtWidgets.QProgressBar()
        self._progress.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        self._progress.setRange(0, 1)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        progress_layout.addWidget(self._progress, 1)

        self._rem_time = QtWidgets.QLabel()
        self._rem_time.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        progress_layout.addWidget(self._rem_time)

        ctrl_layout.addLayout(progress_layout)

        controls = QtWidgets.QWidget()
        controls.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        controls.setLayout(ctrl_layout)
        layout.addWidget(controls)

        layout.addSpacing(30)

        output_layout = QtWidgets.QHBoxLayout()
        output_layout.setSpacing(1)
        output_layout.setContentsMargins(2, 0, 2, 0)

        self._output_device = QtWidgets.QPushButton("D")
        self._output_device.setFlat(True)
        self._output_device.setFixedSize(QtCore.QSize(16, 16))
        output_layout.addWidget(self._output_device)

        self._mute_button = QtWidgets.QPushButton("M")
        self._mute_button.setFlat(True)
        self._mute_button.setCheckable(True)
        self._mute_button.setFixedSize(QtCore.QSize(16, 16))
        self._mute_button.clicked.connect(self.onMute)
        self._mute_button.setEnabled(False)
        output_layout.addWidget(self._mute_button)

        self._volume = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._volume.setRange(self.VOLUME_MINIMUM, self.VOLUME_MAXIMUM)
        self._volume.setTracking(True)
        self._volume.setTickPosition(QtWidgets.QSlider.NoTicks)
        self._volume.setPageStep(self.VOLUME_PAGE_STEP)
        self._volume.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        self._volume.setEnabled(False)
        output_layout.addWidget(self._volume, 1)

        self._output = QtWidgets.QWidget()
        self._output.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Expanding)
        self._output.setFixedWidth(200)
        self._output.setLayout(output_layout)
        layout.addWidget(self._output, 0, QtCore.Qt.AlignRight)

        self.setLayout(layout)

        self._volume.valueChanged.connect(self.onVolumeChanged)

        self._update_timer = QtCore.QTimer()
        self._update_timer.timeout.connect(self.refresh)
        self._update_timer.start(self.UPDATE_MS)

    @property
    def active_device_id(self):
        return self._active_device_id

    @property
    def cpb(self):
        return self._cpb

    def update(self):
        self._spotify = self._main_window.spotify

        self._prev_button.setEnabled(True)
        self._play_pause_button.setEnabled(True)
        self._next_button.setEnabled(True)
        self._volume.setEnabled(True)

        devs = self._spotify.devices()
        self._devices = []
        for d in devs['devices']:
            self._devices.append(d)
            if d['is_active'] is True:
                self._active_device_id = d['id']
                self._volume.setValue(d['volume_percent'])

        self.updateCurrentlyPlaying()

        self._mute_button.setEnabled(True)
        self._saved_volume_value = self._volume.value()
        if self._volume.value() == 0:
            self._mute_button.setChecked(True)
        else:
            self._mute_button.setChecked(False)

    def updateCurrentlyPlaying(self):
        """
        Update information of currently playing track
        """
        self._cpb = self._spotify.current_playback()
        if self._cpb is not None:
            if self._cpb['is_playing'] is True:
                self._main_window._play_pause.setText("Pause")
                self._play_pause_button.setIcon(Assets().pause_icon)
            else:
                self._main_window._play_pause.setText("Play")
                self._play_pause_button.setIcon(Assets().play_icon)

            if self._cpb['currently_playing_type'] == 'episode':
                # FIXME: spotify API does not report what is playing
                # when playing a podcast
                self._episode_name.setText("")
                self._show_name.setText("")
            elif ('item' in self._cpb) and (self._cpb['item'] is not None):
                item = self._cpb['item']
                self._episode_name.setText(item['name'])

                artists = []
                for a in item['artists']:
                    artists.append(a['name'])
                self._show_name.setText(", ".join(artists))

                img_url = item['album']['images'][0]['url']
                self._img = Assets().get(img_url)
                self._img.image_loaded.connect(self.onImageLoaded)

                progress_ms = self._cpb['progress_ms']
                self._curr_time.setText(utils.msToPlayTime(progress_ms))

                remain_ms = item['duration_ms'] - progress_ms
                self._rem_time.setText("- " + utils.msToPlayTime(remain_ms))

                self._progress.setRange(0, item['duration_ms'])
                self._progress.setValue(progress_ms)
            else:
                self._progress.setRange(0, 1)
                self._progress.setValue(0)

    def onImageLoaded(self):
        scaled_img = self._img.scaledToWidth(self.ARTWORK_WD)
        pixmap = QtGui.QPixmap.fromImage(scaled_img)
        self._artwork.setPixmap(pixmap)

    def refresh(self):
        self.updateCurrentlyPlaying()

    def onVolumeUp(self):
        volume = self._volume.value() + self.VOLUME_PAGE_STEP
        self._volume.setValue(min(volume, self.VOLUME_MAXIMUM))

    def onVolumeDown(self):
        volume = self._volume.value() - self.VOLUME_PAGE_STEP
        self._volume.setValue(max(volume, self.VOLUME_MINIMUM))

    def onVolumeChanged(self, value):
        self._spotify.volume(value, device_id=self._active_device_id)

    def onMute(self):
        if self._mute_button.isChecked():
            self._saved_volume_value = self._volume.value()
            self._volume.setValue(0)
        else:
            self._volume.setValue(self._saved_volume_value)

    def onPlayPause(self):
        cpb = self._spotify.current_playback()
        if cpb['is_playing'] is True:
            self._spotify.pause_playback(device_id=self._active_device_id)
            self._play_pause_button.setIcon(Assets().play_icon)
        else:
            self._spotify.start_playback(device_id=self._active_device_id)
            self._play_pause_button.setIcon(Assets().pause_icon)

    def onNext(self):
        self._spotify.next_track(device_id=self._active_device_id)

    def onPrev(self):
        self._spotify.previous_track(device_id=self._active_device_id)
