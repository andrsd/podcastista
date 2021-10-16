from PyQt5 import QtGui
from podcastista import colors


def test_create_palette():
    palette = colors.create_palette()
    assert isinstance(palette, QtGui.QPalette)
