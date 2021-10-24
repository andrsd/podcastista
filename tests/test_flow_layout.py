import platform
import pytest
from unittest.mock import MagicMock
from PyQt5 import QtCore, QtWidgets


if platform.system() == "Darwin":
    @pytest.fixture
    def layout(qtbot, main_window):
        from podcastista.FlowLayout import FlowLayout
        layout = FlowLayout(main_window)
        yield layout

    @pytest.fixture
    def layout_12(qtbot, main_window):
        from podcastista.FlowLayout import FlowLayout
        layout = FlowLayout(main_window, 4, 2, 1)
        yield layout

    def test_init(layout):
        assert len(layout._item_list) == 0
        assert layout._h_space == -1
        assert layout._v_space == -1

    def test_add_item(layout):
        item = MagicMock()
        layout.addItem(item)
        assert len(layout._item_list) == 1

        assert layout.itemAt(0) == item

        assert layout.takeAt(0) == item
        assert layout.takeAt(0) is None

    def test_horz_spacing():
        from podcastista.FlowLayout import FlowLayout
        layout = FlowLayout()
        assert layout.horizontalSpacing() == -1

    def test_horz_spacing_12(layout_12):
        assert layout_12.horizontalSpacing() == 2

    def test_vert_spacing():
        from podcastista.FlowLayout import FlowLayout
        layout = FlowLayout()
        assert layout.verticalSpacing() == -1

    def test_vert_spacing_12(layout_12):
        assert layout_12.verticalSpacing() == 1

    def test_exp_dirs(layout):
        assert layout.expandingDirections() == \
            QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def test_min_size(layout_12):
        item = MagicMock()
        item.minimumSize.return_value = QtCore.QSize(10, 5)
        layout_12.addItem(item)

        assert layout_12.minimumSize() == QtCore.QSize(18, 13)

    def test_do_layout(layout):
        widget = QtWidgets.QWidget()
        layout.addWidget(widget)

        rect = QtCore.QRect(0, 0, 10, 20)
        assert layout._doLayout(rect, False) == 0

    def test_smart_spacing_none(main_window):
        from podcastista.FlowLayout import FlowLayout
        pm = QtWidgets.QStyle.PM_LayoutVerticalSpacing
        layout = FlowLayout()
        assert layout._smartSpacing(pm) == -1

        widget = QtWidgets.QWidget()
        layout = FlowLayout(widget)
        assert layout._smartSpacing(pm) == -1
