import platform
import pytest
from unittest.mock import MagicMock
from PyQt5 import QtWidgets


if platform.system() == "Darwin":
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

    show1 = {
        'id': '1234',
        'name': 'show',
        'images': [
            {'url': 'url-0'},
            {'url': 'url-1'}
        ],
        'publisher': 'publisher',
        'episodes': [episode]
    }
    shows = {
        'items': [
            {'show': show1}
        ]
    }

    @pytest.fixture
    def widget(qtbot, main_window):
        from podcastista.ListenNowTab import ListenNowTab
        widget = ListenNowTab(main_window)
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
        spotify.current_user_saved_shows.return_value = shows
        widget._main_window._spotify = spotify
        widget.fill()
        assert widget._filler.shows == shows

    def test_on_fill_finished(widget):
        widget._filler = MagicMock()
        widget._filler.shows = shows
        widget.onFillFinished()
