import platform
import pytest
from unittest.mock import MagicMock, patch
from PyQt5 import QtWidgets


if platform.system() == "Darwin":
    episode = {
        'release_date': '2020-01-20',
        'name': 'title',
        'resume_point': {
            'fully_played': True,
            'resume_position_ms': 100
        },
        'description': 'Descr',
        'duration_ms': 100,
        'images': [
            {'url': 'url-0'},
            {'url': 'url-1'}
        ]
    }

    @pytest.fixture
    def widget(qtbot, main_window):
        from podcastista.EpisodeWidget import EpisodeWidget
        widget = EpisodeWidget(episode, False, main_window)
        qtbot.addWidget(widget)
        yield widget

    def test_init_wo_artwork(main_window):
        from podcastista.EpisodeWidget import EpisodeWidget
        widget = EpisodeWidget(episode, True, main_window)
        assert isinstance(widget._artwork, QtWidgets.QLabel)

    def test_init(widget, main_window):
        assert widget._episode == episode

    def test_enter_event(widget):
        widget._play = MagicMock()
        e = MagicMock()
        widget.enterEvent(e)
        widget._play.setVisible.assert_called_once_with(True)

    def test_leave_event(widget):
        widget._play = MagicMock()
        e = MagicMock()
        widget.leaveEvent(e)
        widget._play.setVisible.assert_called_once_with(False)

    def test_on_clicked(widget):
        widget._main_window = MagicMock()
        widget.onClicked()
        widget._main_window.viewEpisode.assert_called_once_with(episode)

    def test_on_play(widget):
        widget.play = MagicMock()
        widget.onPlay()
        widget.play.emit.assert_called_once_with(episode)

    @patch('podcastista.EpisodeWidget.EpisodeWidget.onClicked')
    def test_on_title_clicked(click, widget):
        widget.onTitleClicked()
        click.assert_called_once()
