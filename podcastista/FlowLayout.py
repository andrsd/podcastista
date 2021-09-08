"""
Adopted from https://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html
"""

from PyQt5 import QtWidgets, QtCore


class FlowLayout(QtWidgets.QLayout):

    def __init__(self, parent=None, margin=-1, h_spacing=-1, v_spacing=-1):
        if parent is None:
            super().__init__()
        else:
            super().__init__(parent)
        self._item_list = []
        self._h_space = h_spacing
        self._v_space = v_spacing
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self._item_list.append(item)

    def horizontalSpacing(self):
        if self._h_space >= 0:
            return self._h_space
        else:
            return self._smartSpacing(
                QtWidgets.QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._v_space >= 0:
            return self._v_space
        else:
            return self._smartSpacing(
                QtWidgets.QStyle.PM_LayoutVerticalSpacing)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if (index >= 0 and index < len(self._item_list)):
            return self._item_list[index]
        else:
            return None

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()
        size += QtCore.QSize(
            margins.left() + margins.right(),
            margins.top() + margins.bottom())
        return size

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def takeAt(self, index):
        if (index >= 0 and index < len(self._item_list)):
            return self._item_list.pop(index)
        else:
            return None

    def _doLayout(self, rect, test_only):
        margins = self.contentsMargins()
        effective_rect = rect.adjusted(
            +margins.left(), +margins.top(),
            -margins.right(), -margins.bottom())
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0

        for item in self._item_list:
            wid = item.widget()
            space_x = self.horizontalSpacing()
            if space_x == -1:
                space_x = wid.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton,
                    QtCore.Qt.Horizontal)
            space_y = self.verticalSpacing()
            if space_y == -1:
                space_y = wid.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton,
                    QtCore.Qt.Vertical)
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > effective_rect.right() and line_height > 0:
                x = effective_rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QtCore.QRect(
                    QtCore.QPoint(x, y),
                    item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y() + margins.bottom()

    def _smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()
