import platform
import pytest
from unittest.mock import MagicMock


if platform.system() == "Darwin":
    @pytest.fixture
    def widget(qtbot, main_window):
        from podcastista.EpisodeDetails import EpisodeDetails
        widget = EpisodeDetails(main_window)
        qtbot.addWidget(widget)
        yield widget

    def test_init(widget, main_window):
        assert widget._main_window == main_window
        assert widget._episode is None
        assert widget._follow_button is None

    def test_id(widget):
        widget._episode = None
        assert widget.id is None

        widget._episode = {'id': '1234'}
        assert widget.id == '1234'

    def test_fill(widget):
        widget._img = MagicMock()
        episode = {
            'images': [
                {'url': 'url-0'},
                {'url': 'url-1'}
            ],
            'duration_ms': 100,
            'release_date': '2020-01-02',
            'name': 'title',
            'description': 'description',
            'language': 'en',
            'explicit': False,
            'resume_point': {
                'fully_played': True,
                'resume_position_ms': 100
            }
        }
        widget.fill(episode)

        assert widget._episode == episode
        assert widget._title.text() == 'title'
        assert widget._description.text() == 'description'
        assert widget._play.text() == '\u25B6  Play Again'
        assert widget._play.isEnabled() is True

    def test_on_back(widget):
        widget._main_window = MagicMock()
        widget.onBack()
        widget._main_window.onBack.assert_called_once()

    def test_on_vert_scroll_small(widget):
        widget.onVertScroll(10)
        assert widget._episode_label.text() == ""

    def test_on_vert_scroll_large(widget):
        widget._episode = {
            'name': 'title'
        }
        widget.onVertScroll(100)
        assert widget._episode_label.text() == "title"

    def test_on_play(widget):
        widget._main_window = MagicMock()
        widget._episode = {'uri': 'uri-0'}
        widget.onPlay()
        widget._main_window.startPlayback.assert_called_once_with(['uri-0'])
