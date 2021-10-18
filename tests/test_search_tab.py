import platform
import pytest
from unittest.mock import MagicMock
from PyQt5 import QtWidgets


if platform.system() == "Darwin":
    @pytest.fixture
    def widget(qtbot, main_window):
        from podcastista.SearchTab import SearchTab
        widget = SearchTab(main_window)
        widget._main_window._spotify = MagicMock()
        qtbot.addWidget(widget)
        yield widget

    def test_init(widget):
        from podcastista.FlowLayout import FlowLayout
        assert isinstance(widget._shows_layout, FlowLayout)

    # @patch('podcastista.SearchTab.SearchThread')
    def test_search(widget):
        widget.search("text")

    def test_clear(widget):
        widget._shows_layout.addWidget(QtWidgets.QWidget())
        widget._episodes_layout.addWidget(QtWidgets.QWidget())
        widget._layout.addWidget(QtWidgets.QWidget())
        widget.clear()

    def test_on_search_finished(widget):
        show = {
            'id': '1234',
            'name': 'show',
            'images': [
                {'url': 'url-0'},
                {'url': 'url-1'}
            ],
            'publisher': 'publisher',
        }

        episode = {
            'resume_point': {
                'resume_position_ms': 100,
                'fully_played': True
            },
            'duration_ms': 100,
            'release_date': '2020-10-22',
            'name': 'episode',
            'uri': 'episode-uri',
            'images': [
                {'url': 'url-0'},
                {'url': 'url-1'}
            ],
            'description': 'descr'
        }

        widget._layout.addWidget(QtWidgets.QWidget())
        widget._searcher = MagicMock()
        widget._searcher.shows = {
            'shows': {
                'items': [
                    show,
                    show
                ]
            }
        }
        widget._searcher.episodes = {
            'episodes': {
                'items': [
                    episode,
                    episode
                ]
            }
        }

        widget.onSearchFinished()

        assert widget._episodes_layout.count() == 4
        assert widget._shows_layout.count() == 2
        assert widget._layout.count() == 5

    def test_on_play_episode(widget):
        ep = {
            'uri': 'ep-uri'
        }
        widget._main_window = MagicMock()
        widget.onPlayEpisode(ep)
        widget._main_window.startPlayback.assert_called_once_with(['ep-uri'])
