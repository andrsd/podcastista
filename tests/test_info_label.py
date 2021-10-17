import platform
import pytest
from PyQt5 import QtWidgets


if platform.system() == "Darwin":
    @pytest.fixture
    def info_label(qtbot, main_window):
        from podcastista.InfoLabel import InfoLabel
        widget = InfoLabel("title", "text", main_window)
        qtbot.addWidget(widget)
        yield widget

    def test_init(info_label):
        assert info_label._title.text() == "title"
        assert info_label._text.text() == "text"
        assert info_label.sizePolicy() == QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)

    def test_set(info_label):
        info_label.set("new_text")
        assert info_label._text.text() == "new_text"
