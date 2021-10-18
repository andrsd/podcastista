import platform
import pytest
from unittest.mock import MagicMock, patch
from PyQt5 import QtWidgets


if platform.system() == "Darwin":
    episode1 = {
        'resume_point': {
            'resume_position_ms': 0,
            'fully_played': False
        },
        'duration_ms': 100,
        'release_date': '2020-10-22',
        'name': 'episode',
        'uri': 'episode-uri',
        'images': [
            {'url': 'url-0'},
            {'url': 'url-1'}
        ],
        'description': 'descr',
        'id': 'e1'
    }
    episode2 = {
        'resume_point': {
            'resume_position_ms': 100,
            'fully_played': True
        },
        'duration_ms': 200,
        'release_date': '2020-10-23',
        'name': 'episode',
        'uri': 'episode-uri',
        'images': [
            {'url': 'url-0'},
            {'url': 'url-1'}
        ],
        'description': 'descr',
        'id': 'e2'
    }

    show1 = {
        'id': '1234',
        'name': 'show',
        'images': [
            {'url': 'url-0'},
            {'url': 'url-1'}
        ],
        'publisher': 'publisher',
        'episodes': {
            'items': [episode1, episode2]
        }
    }
    shows = {
        'items': [
            {'show': show1}
        ]
    }

    @pytest.fixture
    def widget(qtbot, main_window):
        from podcastista.LatestEpisodesListTab import LatestEpisodesListTab
        widget = LatestEpisodesListTab(main_window)
        qtbot.addWidget(widget)
        yield widget

    def test_init(widget):
        assert isinstance(widget._stacked_layout, QtWidgets.QStackedLayout)

    def test_clear(widget):
        widget._layout.addWidget(QtWidgets.QWidget())
        widget.clear()
        assert widget._layout.count() == 0

    def test_fill(widget):
        spotify = MagicMock()
        spotify.show_episodes.return_value = {
            'items': [episode1, episode2]
        }
        widget._main_window._spotify = spotify
        widget._layout = MagicMock()
        widget._layout.count.return_value = 2
        widget.fill(shows)
        widget._filler.finished.disconnect()
        widget._filler.run()
        widget._filler.wait()
        widget.onFillFinished()

        assert len(widget._episodes) == 1
        assert widget._layout.addWidget.call_count == 2

    @patch('podcastista.MainWindow.MainWindow.startPlayback')
    def test_on_play_from_episode(start, widget):
        widget._episode_idx = {
            episode1['id']: 0
        }
        widget._episodes = [episode1]
        widget.onPlayFromEpisode(episode1)
        start.assert_called_once_with([episode1['uri']])
