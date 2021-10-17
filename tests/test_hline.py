import platform
from PyQt5 import QtWidgets
from podcastista.HLine import HLine


if platform.system() == "Darwin":
    def test_init(main_window):
        widget = HLine(main_window)

        assert widget.frameShape() == QtWidgets.QFrame.HLine
        assert widget.frameShadow() == QtWidgets.QFrame.Plain
