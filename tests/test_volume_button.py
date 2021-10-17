import pytest
from unittest.mock import patch
from PyQt5 import QtCore


@pytest.fixture
def volume_button(qtbot):
    from podcastista.VolumeButton import VolumeButton
    button = VolumeButton()
    qtbot.addWidget(button)
    yield button


def test_init(volume_button):
    assert volume_button.isFlat() is True
    assert volume_button.isCheckable() is True
    assert volume_button.size() == QtCore.QSize(20, 20)


def test_set_size(volume_button):
    volume_button.setSize(QtCore.QSize(30, 30))
    assert volume_button.iconSize() == QtCore.QSize(30, 30)


def test_update_icon(volume_button):
    volume_button.setChecked(True)
    volume_button.updateIcon()
    # assert volume_button.icon() == Assets().volume_muted_icon

    volume_button.setChecked(False)
    volume_button.updateIcon()
    # assert volume_button.icon() == Assets().volume_on_icon


@patch('podcastista.VolumeButton.VolumeButton.updateIcon')
def test_on_clicked(update, volume_button):
    volume_button.onClicked()
    update.assert_called_once()
