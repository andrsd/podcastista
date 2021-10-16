from PyQt5 import QtGui
from unittest.mock import MagicMock, patch
from podcastista.assets import NetworkImage


def test_network_image():
    ni = NetworkImage()
    assert isinstance(ni._img, QtGui.QImage)


@patch('PyQt5.QtGui.QImage.load')
def test_network_image_load(load):
    device = MagicMock()
    format = MagicMock()
    ni = NetworkImage()
    ni.load(device, format)
    load.assert_called_once()


def test_network_image_done():
    ni = NetworkImage()
    ni.done()


def test_network_image_scaled_to_width_none():
    ni = NetworkImage()
    ni._img = MagicMock()
    ni._img.isNull.return_value = True
    img = ni.scaledToWidth(100)
    assert isinstance(img, QtGui.QImage)


def test_network_image_scaled_to_width():
    ni = NetworkImage()
    ni._img = MagicMock()
    ni._img.isNull.return_value = False
    ni.scaledToWidth(100)
    ni._img.scaledToWidth.assert_called_once_with(100)


def test_singleton():
    # assert Assets() is Assets()
    # assert Assets().app_icon is Assets().app_icon
    # assert Assets().prev_icon is Assets().prev_icon
    # assert Assets().next_icon is Assets().next_icon
    # assert Assets().play_icon is Assets().play_icon
    # assert Assets().pause_icon is Assets().pause_icon
    pass


def test_icons():
    # assert isinstance(Assets().app_icon, QtGui.QIcon)
    # assert isinstance(Assets().prev_icon, QtGui.QIcon)
    # assert isinstance(Assets().next_icon, QtGui.QIcon)
    # assert isinstance(Assets().play_icon, QtGui.QIcon)
    # assert isinstance(Assets().pause_icon, QtGui.QIcon)
    pass
