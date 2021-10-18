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
        'episodes': [
            {
                'resume_point': {
                    'resume_position_ms': 100,

                },
                'duration_ms': 100,
                'release_date': '2020-10-22',
                'name': 'episode',
                'uri': 'episode-uri'
            },
            {}
        ]
    }

    @pytest.fixture
    def widget(qtbot, main_window):
        from podcastista.ShowEpisodeWidget import ShowEpisodeWidget
        widget = ShowEpisodeWidget(show, main_window)
        qtbot.addWidget(widget)
        yield widget

    def test_init(widget):
        assert widget._show == show
        assert widget._episode_name.text() == 'episode'
        assert widget._title.text() == 'show'

    @patch('PyQt5.QtWidgets.QWidget.mouseReleaseEvent')
    @patch('podcastista.ShowEpisodeWidget.ShowEpisodeWidget.onClicked')
    def test_mouse_release_event(clicked, release, widget):
        e = MagicMock()
        e.button.return_value = QtCore.Qt.LeftButton
        e.pos.return_value = QtCore.QPoint(10, 10)
        widget.mouseReleaseEvent(e)
        clicked.assert_called_once()

        e.pos.return_value = QtCore.QPoint(-1, -1)
        widget.mouseReleaseEvent(e)
        release.assert_called_once()

    def test_enter_event(widget):
        e = MagicMock()
        widget._controls = MagicMock()
        widget._play_btn = MagicMock()
        widget.enterEvent(e)
        widget._controls.setCurrentWidget.assert_called_once()
        widget._play_btn.setVisible.assert_called_once_with(True)

    def test_leave_event(widget):
        e = MagicMock()
        widget._controls = MagicMock()
        widget._play_btn = MagicMock()
        widget.leaveEvent(e)
        widget._controls.setCurrentWidget.assert_called_once()
        widget._play_btn.setVisible.assert_called_once_with(False)

    @patch('podcastista.ShowEpisodeWidget.ShowEpisodeWidget.onShowNameClicked')
    def test_on_clicked(click, widget):
        widget._main_window = MagicMock()
        widget.onClicked()
        click.assert_called_once()

    def test_on_image_loaded(widget):
        widget._artwork = MagicMock()
        widget.onImageLoaded()
        widget._artwork.setPixmap.assert_called_once()

    def test_on_episode_name_clicked(widget):
        widget._main_window = MagicMock()
        widget.onEpisodeNameClicked()
        widget._main_window.viewEpisode.assert_called_once()

    def test_on_show_name_clicked(widget):
        widget._main_window = MagicMock()
        widget.onShowNameClicked()
        widget._main_window.viewShow.assert_called_once_with('1234')

    def test_on_play(widget):
        mw = MagicMock()
        widget._main_window = mw
        widget.onPlay()
        mw.startPlayback.assert_called_once_with(['episode-uri'])
