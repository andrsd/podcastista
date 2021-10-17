import platform
import pytest
from unittest.mock import MagicMock, patch
from PyQt5 import QtGui, QtCore


if platform.system() == "Darwin":
    normal_icon = QtGui.QIcon()
    selected_icon = QtGui.QIcon()

    @pytest.fixture
    def play_button(qtbot, main_window):
        from podcastista.EpisodePlayButton import EpisodePlayButton
        widget = EpisodePlayButton(normal_icon, selected_icon, main_window)
        qtbot.addWidget(widget)
        yield widget

    def test_init(play_button):
        assert play_button.isFlat() is True
        assert play_button.size() == QtCore.QSize(32, 32)

    @patch('podcastista.EpisodePlayButton.EpisodePlayButton.setIcon')
    def test_enter_event(set_icon, play_button):
        e = MagicMock()
        play_button.enterEvent(e)
        set_icon.assert_called_once_with(selected_icon)

    @patch('podcastista.EpisodePlayButton.EpisodePlayButton.setIcon')
    def test_leave_event(set_icon, play_button):
        e = MagicMock()
        play_button.leaveEvent(e)
        set_icon.assert_called_once_with(normal_icon)
