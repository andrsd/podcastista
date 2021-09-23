from PyQt5 import QtGui

from podcastista.assets import Assets


def test_singleton():
    assert Assets() is Assets()
    assert Assets().prev_icon is Assets().prev_icon
    assert Assets().next_icon is Assets().next_icon
    assert Assets().play_icon is Assets().play_icon
    assert Assets().pause_icon is Assets().pause_icon
    assert Assets().devices_icon is Assets().devices_icon
    assert Assets().spotify_logo is Assets().spotify_logo


def test_has_logo():
    assert isinstance(Assets().prev_icon, QtGui.QIcon)
    assert isinstance(Assets().next_icon, QtGui.QIcon)
    assert isinstance(Assets().play_icon, QtGui.QIcon)
    assert isinstance(Assets().pause_icon, QtGui.QIcon)
    assert isinstance(Assets().devices_icon, QtGui.QIcon)
    assert isinstance(Assets().spotify_logo, QtGui.QIcon)
