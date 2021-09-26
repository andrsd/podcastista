from PyQt5 import QtGui


COLORS = {
    # Qt:
    'Active:Base': (60, 60, 60),
    'Active:Window': (40, 40, 40),
    'Active:Button': (40, 40, 40),
    'Active:Text': (200, 200, 200),
    'Active:HighlightedText': (255, 255, 255),
    'Active:WindowText': (200, 200, 200),
    'Active:ButtonText': (200, 200, 200),
    'Active:Highlight': (48, 123, 246),
    'Active:Link': (48, 123, 246),
    'Disabled:Light': (0, 0, 0, 0),
    'Disabled:Text': (140, 140, 140),
}


def create_palette():
    """Create a palette from a config dictionary. Keys are a string of
    'ColourGroup:ColorRole' and values are a (r, g, b) tuple. E.g:
    {
        'Active:WindowText': (80, 100, 0),
        ...
    }

    Colors from the Active group will automatically be applied to the
    Inactive group as well. Unknown color groups will be ignored.
    """

    palette = QtGui.QPalette()
    for key, value in COLORS.items():
        group, role = key.split(':')
        if hasattr(QtGui.QPalette.ColorGroup, group):
            palette.setColor(
                getattr(QtGui.QPalette.ColorGroup, group),
                getattr(QtGui.QPalette.ColorRole, role),
                QtGui.QColor(*value))
            if group == 'Active':
                # Also set the Inactive colour group.
                palette.setColor(
                    QtGui.QPalette.ColorGroup.Inactive,
                    getattr(QtGui.QPalette.ColorRole, role),
                    QtGui.QColor(*value))

    return palette
