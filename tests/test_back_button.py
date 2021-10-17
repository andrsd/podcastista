import platform
import pytest
from PyQt5 import QtCore


if platform.system() == "Darwin":
    @pytest.fixture
    def back_button(qtbot, main_window):
        from podcastista.BackButton import BackButton
        button = BackButton(main_window)
        qtbot.addWidget(button)
        yield button

    def test_init(back_button):
        assert back_button.isFlat() is True
        assert back_button.isCheckable() is False
        assert back_button.minimumSize() == QtCore.QSize(30, 28)
        assert back_button.maximumSize() == QtCore.QSize(30, 28)
