from PyQt5 import QtWidgets, QtCore, QtGui

class ShowEpisodeList(QtWidgets.QWidget):
    """
    List of all epsiodes in a show
    """

    def __init__(self, parent):
        super().__init__()
        self._main_window = parent
