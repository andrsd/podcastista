import platform
import pytest
from unittest.mock import MagicMock
from PyQt5 import QtWidgets


if platform.system() == "Darwin":
    @pytest.fixture
    def widget(qtbot, main_window):
        from podcastista.ShowsTab import ShowsTab
        widget = ShowsTab(main_window)
        qtbot.addWidget(widget)
        yield widget

    def test_init(widget):
        assert widget._shows == []

    def test_show(widget):
        sh = [
            1, 2, 3
        ]
        widget._shows = sh
        assert widget.shows == sh

    def test_clear(widget):
        widget._layout.addWidget(QtWidgets.QWidget())
        widget.clear()
        assert widget._layout.count() == 0

    def test_fill(widget):
        show = {
            'id': '1234',
            'name': 'show',
            'images': [
                {'url': 'url-0'},
                {'url': 'url-1'}
            ],
            'publisher': 'publisher',
        }

        spotify = MagicMock()
        spotify.current_user_saved_shows.return_value = {
            'items': [
                {'show': show},
                {'show': show}
            ]
        }
        widget._main_window._spotify = spotify
        widget._layout = MagicMock()
        widget._layout.count.return_value = 2
        widget.fill()
        assert widget._layout.addWidget.call_count == 2
