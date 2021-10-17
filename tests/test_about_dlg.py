import platform
from podcastista.AboutDialog import AboutDialog


if platform.system() == "Darwin":
    def test_init(main_window):
        dlg = AboutDialog(main_window)
        assert dlg._title.text() == "Podcastista"
        assert dlg.windowTitle() == "About"
