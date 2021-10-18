import platform
import pytest
from unittest.mock import MagicMock, patch
from PyQt5 import QtCore


if platform.system() == "Darwin":
    show = {
        'id': '1234',
        'name': 'show',
        'images': [
            {'url': 'url-0'},
            {'url': 'url-1'}
        ],
        'publisher': 'publisher',

    }

    @pytest.fixture
    def widget(qtbot, main_window):
        from podcastista.ShowWidget import ShowWidget
        widget = ShowWidget(show, main_window)
        qtbot.addWidget(widget)
        yield widget

    def test_init(widget):
        assert widget._show == show
        assert widget._title.text() == 'show'
        assert widget._author.text() == 'publisher'

    @patch('PyQt5.QtWidgets.QWidget.mouseReleaseEvent')
    @patch('podcastista.ShowWidget.ShowWidget.onClicked')
    def test_mouse_release_event(clicked, release, widget):
        e = MagicMock()
        e.button.return_value = QtCore.Qt.LeftButton
        e.pos.return_value = QtCore.QPoint(10, 10)
        widget.mouseReleaseEvent(e)
        clicked.assert_called_once()

        e.pos.return_value = QtCore.QPoint(-1, -1)
        widget.mouseReleaseEvent(e)
        release.assert_called_once()

    def test_on_clicked(widget):
        widget._main_window = MagicMock()
        widget.onClicked()
        widget._main_window.viewShow.assert_called_once_with('1234')

    def test_on_image_loaded(widget):
        widget._artwork = MagicMock()
        widget.onImageLoaded()
        widget._artwork.setPixmap.assert_called_once()
