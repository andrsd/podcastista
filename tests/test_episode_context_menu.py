import platform
from unittest.mock import MagicMock
from PyQt5 import QtGui
from podcastista.EpisodeContextMenu import EpisodeContextMenu


if platform.system() == "Darwin":
    def test_init():
        main_window = MagicMock()
        episode = {
            'external_urls': {
                'spotify': 'my_url'
            }
        }
        menu = EpisodeContextMenu(main_window, episode)
        assert menu._uri == "my_url"

        menu = EpisodeContextMenu(main_window, [])
        assert menu._uri is None

    def test_on_add_to_queue():
        episode = {
            'external_urls': {
                'spotify': 'my_url'
            }
        }
        main_window = MagicMock()
        menu = EpisodeContextMenu(main_window, episode)
        menu.onAddToQueue()

        main_window.addToQueue.assert_called_once_with('my_url')
        main_window.showNotification.assert_called_once_with('Added to queue')

    def test_on_click_link():
        episode = {
            'external_urls': {
                'spotify': 'my_url'
            }
        }
        main_window = MagicMock()
        menu = EpisodeContextMenu(main_window, episode)
        menu.onCopyLink()

        clipboard = QtGui.QGuiApplication.clipboard()
        assert clipboard.text() == 'my_url'
        main_window.showNotification.assert_called_once_with(
            'Link copied to clipboard')
