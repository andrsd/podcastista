import platform
import pytest
from unittest.mock import MagicMock, patch


if platform.system() == "Darwin":
    @pytest.fixture
    def widget(qtbot, main_window):
        from podcastista.ShowDetails import ShowDetails
        w = ShowDetails(main_window)
        yield w

    def test_init(widget):
        from podcastista.BackButton import BackButton

        assert widget._show is None
        assert isinstance(widget._back, BackButton)

    def test_id(widget):
        assert widget.id is None

        widget._show = {'id': 1234}
        assert widget.id == 1234

    def test_active_page(widget):
        widget._stacked_widget = MagicMock()
        widget._stacked_widget.currentIndex.return_value = 5
        assert widget.active_page == 5

    def test_set_active_page(widget):
        widget._stacked_widget = MagicMock()
        widget.setActivePage(2)
        widget._stacked_widget.setCurrentIndex.assert_called_once_with(2)

    def test_fill(widget):
        show = {
            'id': '1234',
            'name': 'show',
            'images': [
                {'url': 'url-0'},
                {'url': 'url-1'}
            ],
            'publisher': 'publisher',
            'total_episodes': 1,
            'languages': ['cz'],
            'explicit': False,
            'episodes': {
                'items': [
                    {
                        'resume_point': {
                            'resume_position_ms': 100,
                            'fully_played': False
                        },
                        'duration_ms': 100,
                        'release_date': '2020-10-22',
                        'name': 'episode',
                        'uri': 'episode-uri',
                        'description': 'descr-0'
                    }
                ]
            }
        }
        spotify = MagicMock()
        spotify.show.return_value = show
        widget._main_window._spotify = spotify

        widget.fill(1234)

    def test_on_back(widget):
        widget._stacked_widget = MagicMock()
        widget._main_window = MagicMock()
        widget.onBack()
        widget._main_window.onBack.assert_called_once()

    @patch('podcastista.ShowDetails.ShowDetails._updateShowLabel')
    def test_on_back_2(updt, widget):
        list_widget = MagicMock()
        widget._list_widget = list_widget
        widget._stacked_widget = MagicMock()
        widget._stacked_widget.currentWidget.return_value = list_widget
        widget._main_window = MagicMock()
        widget._info_widget = MagicMock()
        widget.onBack()
        widget._stacked_widget.setCurrentWidget.assert_called_once()
        updt.assert_called_once()

    def test_on_follow_clicked(widget):
        widget._show = {'id': 1234}
        main_wnd = MagicMock()
        widget._main_window = main_wnd

        widget._following = True
        widget.onFollowClicked()
        main_wnd.unfollowShow.assert_called_once_with(1234)

        widget._following = False
        widget.onFollowClicked()
        main_wnd.followShow.assert_called_once_with(1234)

    def test_update_follow_state(widget):
        widget._show = {'id': '1234'}
        spotify = MagicMock()
        spotify.current_user_saved_shows_contains.return_value = [False]
        widget._main_window._spotify = spotify
        widget.updateFollowState()
        assert widget._follow_button.text() == "Follow"

        spotify.current_user_saved_shows_contains.return_value = [True]
        widget._main_window._spotify = spotify
        widget.updateFollowState()
        assert widget._follow_button.text() == "Following"

    @patch('podcastista.ShowDetails.ShowDetails._updateShowLabel')
    def test_on_vert_scroll(update, widget):
        widget.onVertScroll(10)
        update.assert_called_once_with(10)

    def test_update_show_label(widget):
        widget._updateShowLabel(50)
        assert widget._show_label.text() == ""

        widget._show = {
            'id': '1234',
            'name': 'show-name'
        }
        widget._show_label = MagicMock()
        widget._updateShowLabel(90)
        widget._show_label.setStyleSheet.assert_called_once()

    def test_on_play_latest(widget):
        widget._show = {
            'id': '1234',
            'name': 'show-name',
            'episodes': {
                'items': [{'uri': 'uri-uri'}]
            }
        }
        widget._main_window = MagicMock()
        widget.onPlayLatest()
        widget._main_window.startPlayback.assert_called_once_with(['uri-uri'])

    def test_get_episodes_from_id(widget):
        episodes = [
            {
                'id': '1',
                'uri': 'uri1'
            },
            {
                'id': '2',
                'uri': 'uri2'
            }
        ]
        uris = widget._getEpisodesFromId(episodes, '2')
        assert uris == ['uri2']

    @patch('podcastista.ShowDetails.ShowDetails._getEpisodesFromId')
    def test_on_play_from_episode(gefid, widget):
        widget._show = {
            'id': '1234',
            'name': 'show-name',
            'episodes': {
                'items': [{'uri': 'uri-0'}]
            }
        }
        gefid.return_value = ['uri-0', 'uri-1']
        widget._main_window = MagicMock()
        ep = MagicMock()
        widget.onPlayFromEpisode(ep)
        gefid.assert_called_once()
        widget._main_window.startPlayback.assert_called_once_with(
            ['uri-0', 'uri-1'])

    @patch('podcastista.ShowDetails.ShowDetails._getEpisodesFromId')
    def test_on_play_from_episode_all(gefid, widget):
        widget._show = {
            'id': '1234',
            'name': 'show-name',
            'episodes': {
                'items': [{'uri': 'uri-0'}]
            }
        }
        gefid.return_value = ['uri-0', 'uri-1']
        widget._main_window = MagicMock()
        ep = MagicMock()
        widget.onPlayFromEpisodeAll(ep)
        gefid.assert_called_once()
        widget._main_window.startPlayback.assert_called_once_with(
            ['uri-0', 'uri-1'])

    @patch('podcastista.ShowDetails.ShowDetails._updateShowLabel')
    def test_on_see_all_episodes(widget):
        widget._stacked_widget = MagicMock()
        widget.onSeeAllEpisodes()
