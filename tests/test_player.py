import platform
import pytest
from unittest.mock import MagicMock, patch
from PyQt5 import QtGui


if platform.system() == "Darwin":
    @pytest.fixture
    def player(qtbot, main_window):
        from podcastista.Player import Player
        w = Player(main_window)
        yield w

    def test_update(player):
        dev = {
            'name': 'dev',
            'id': 321,
            'volume_percent': 90,
            'is_active': True
        }
        spotify = MagicMock()
        spotify.devices.return_value = {
            'devices': [dev]
        }

        player._main_window._spotify = spotify
        player.update()
        assert player._devices[0] == dev

    def test_update_currently_playing_episode(player):
        spotify = MagicMock()
        spotify.current_playback.return_value = {
            'is_playing': True,
            'currently_playing_type': 'episode'
        }
        player._spotify = spotify
        player.updateCurrentlyPlaying()
        assert player._episode_name.text() == ""
        assert player._show_name.text() == ""

    def test_update_currently_playing_item(player):
        spotify = MagicMock()
        spotify.current_playback.return_value = {
            'is_playing': True,
            'progress_ms': 1000,
            'currently_playing_type': 'track',
            'item': {
                'name': 'name',
                'duration_ms': 10000,
                'artists': [
                    {
                        'name': 'aname'
                    }
                ],
                'album': {
                    'images': [
                        {
                            'url': 'url'
                        }
                    ]
                }
            }
        }
        player._spotify = spotify
        player.updateCurrentlyPlaying()
        assert player._progress.value() == 1000

    def test_on_image_loaded(player):
        img = MagicMock()
        img.scaledToWidth.return_value = QtGui.QImage()
        player._img = img
        player.onImageLoaded()
        img.scaledToWidth.assert_called_once()

    @patch('podcastista.Player.Player.updateCurrentlyPlaying')
    def test_refresh(update, player):
        player.refresh()
        update.assert_called_once()

    def test_on_volume_up(player):
        player.onVolumeUp()
        assert player._volume.value() == 6

    def test_on_volume_down(player):
        player.onVolumeDown()
        assert player._volume.value() == 0

    def test_on_mute(player):
        player._mute_button.setChecked(True)
        player.onMute()
        assert player._volume.value() == 0

    def test_on_mute_restore(player):
        player._saved_volume_value = 10
        player._mute_button.setChecked(False)
        player.onMute()
        assert player._volume.value() == 10

    def test_play_pause(player):
        spotify = MagicMock()
        spotify.current_playback.return_value = {
            'is_playing': True
        }
        player._active_device_id = 1234
        player._spotify = spotify
        player.onPlayPause()

        spotify.pause_playback.assert_called_once_with(device_id=1234)

    def test_play_pause_2(player):
        spotify = MagicMock()
        spotify.current_playback.return_value = {
            'is_playing': False
        }
        player._active_device_id = 1234
        player._spotify = spotify
        player.onPlayPause()

        spotify.start_playback.assert_called_once_with(device_id=1234)

    def test_on_next(player):
        spotify = MagicMock()
        player._spotify = spotify
        player._active_device_id = 1234
        player.onNext()
        spotify.next_track.assert_called_once_with(device_id=1234)

    def test_on_prev(player):
        spotify = MagicMock()
        player._spotify = spotify
        player._active_device_id = 1234
        player.onPrev()
        spotify.previous_track.assert_called_once_with(device_id=1234)

    def test_on_device_selected(player):
        player._device_actions = [21, 42]
        player._devices = [
            {
                'id': 1212
            },
            {
                'id': 4242
            }
        ]
        player.onDeviceSelected(42)
        assert player._active_device_id == 4242

    def test_set_active_device(player):
        player._spotify = MagicMock()
        player._device_actions = [MagicMock(), MagicMock()]
        player._devices = [
            {
                'id': 1212,
                'volume_percent': 12
            },
            {
                'id': 4242,
                'volume_percent': 42
            }
        ]
        player.setActiveDevice(4242)
        assert player._active_device_id == 4242
        assert player._volume.value() == 42
