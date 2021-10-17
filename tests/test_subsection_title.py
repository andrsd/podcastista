import platform
from PyQt5 import QtWidgets
from podcastista.SubsectionTitle import SubsectionTitle


if platform.system() == "Darwin":
    def test_init(main_window):
        title = SubsectionTitle("text", main_window)

        assert title.text() == "text"
        assert title.sizePolicy() == QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
