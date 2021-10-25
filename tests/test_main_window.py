import platform
from unittest.mock import MagicMock, patch


if platform.system() == "Darwin":

    @patch('podcastista.Player.Player.onPlayPause')
    def test_on_play_pause(play_pause, main_window):
        main_window._player._cpb = None
        main_window.onPlayPause()
        play_pause.assert_not_called()

    @patch('podcastista.Player.Player.onPlayPause')
    def test_on_play_pause_1(play_pause, main_window):
        main_window._player._cpb = {'is_playing': True}
        main_window.onPlayPause()
        assert main_window._play_pause.text() == "Play"
        play_pause.assert_called_once()

    @patch('podcastista.Player.Player.onPlayPause')
    def test_on_play_pause_2(play_pause, main_window):
        main_window._player._cpb = {'is_playing': False}
        main_window.onPlayPause()
        assert main_window._play_pause.text() == "Pause"
        play_pause.assert_called_once()

    def test_on_about(main_window):
        from podcastista.AboutDialog import AboutDialog
        main_window.onAbout()
        assert isinstance(main_window._about_dlg, AboutDialog)

    @patch('podcastista.MainWindow.MainWindow.showMinimized')
    def test_on_minimize(minim, main_window):
        main_window.onMinimize()
        minim.assert_called_once()

    @patch('podcastista.MainWindow.MainWindow.isMaximized')
    @patch('podcastista.MainWindow.MainWindow.showNormal')
    @patch('podcastista.MainWindow.MainWindow.showMaximized')
    def test_on_zoom(maxim, norm, is_max, main_window):
        is_max.return_value = True
        main_window.onZoom()
        norm.assert_called_once()

        is_max.return_value = False
        main_window.onZoom()
        maxim.assert_called_once()

    @patch('podcastista.MainWindow.MainWindow.showNormal')
    def test_on_brinf_all_to_front(norm, main_window):
        main_window.onBringAllToFront()
        norm.assert_called_once()

    @patch('podcastista.MainWindow.MainWindow.showNormal')
    def test_on_show_main_window(norm, main_window):
        main_window.onShowMainWindow()
        norm.assert_called_once()

    def test_close_event(main_window):
        event = MagicMock()
        main_window.closeEvent(event)
        event.accept.assert_called_once()

    def test_spotify(main_window):
        spotify = MagicMock()
        main_window._spotify = spotify
        assert main_window.spotify == spotify

    def test_connect_to_spotify(main_window):
        main_window._nam = MagicMock()
        main_window.connectToSpotify()
        main_window._nam.get.assert_called_once()

    @patch('podcastista.MainWindow.MainWindow.errorCannotConnectToSpotify')
    def test_setup_spotify_empty(err, main_window):
        main_window.setupSpotify(None)
        err.assert_called_once()

    @patch('podcastista.MainWindow.MainWindow.loadData')
    @patch('podcastista.MainWindow.MainWindow.updateMenuBar')
    def test_setup_spotify(load, update, main_window):
        spotify = MagicMock()
        main_window.setupSpotify(spotify)
        update.assert_called_once()
        load.assert_called_once()

    def test_restrore_state(main_window):
        main_window._player._devices = MagicMock()
        main_window._restoreState()

    def test_on_network_reply(main_window):
        reply = MagicMock()
        reply.url().host.return_value = "localhost"
        main_window.onNetworkReply(reply)

    @patch('PyQt5.QtWidgets.QMessageBox.exec')
    def test_report_unkn_dev(exec, main_window):
        main_window.reportUnknownDeviceId()
        exec.assert_called_once()

    @patch('PyQt5.QtWidgets.QMessageBox.exec')
    def test_error_cant_connect_to_spotify(exec, main_window):
        main_window.errorCannotConnectToSpotify()
        exec.assert_called_once()

    @patch('podcastista.ShowsTab.ShowsTab.clear')
    @patch('podcastista.LatestEpisodesListTab.LatestEpisodesListTab.clear')
    @patch('podcastista.ListenNowTab.ListenNowTab.clear')
    def test_clear_data(cl1, cl2, cl3, main_window):
        main_window.clearData()
        cl1.assert_called_once()
        cl2.assert_called_once()
        cl3.assert_called_once()

    @patch('podcastista.ShowsTab.ShowsTab.fill')
    @patch('podcastista.ListenNowTab.ListenNowTab.fill')
    def test_load_data(fill1, fill2, main_window):
        main_window.loadData()
        fill1.assert_called_once()
        fill2.assert_called_once()

    def test_on_view_episodes(main_window):
        ep = MagicMock()
        main_window._left_latest_episodes = ep
        main_window.onViewEpisodes()
        ep.setChecked.assert_called_once_with(True)

    def test_on_view_show(main_window):
        ep = MagicMock()
        main_window._left_shows = ep
        main_window.onViewShows()
        ep.setChecked.assert_called_once_with(True)

    def test_on_view_listen_now(main_window):
        ep = MagicMock()
        main_window._left_listen_now = ep
        main_window.onViewListenNow()
        ep.setChecked.assert_called_once_with(True)

    @patch('podcastista.ShowDetails.ShowDetails.fill')
    def test_view_show(fill, main_window):
        stacked_layout = MagicMock()
        stacked_layout.currentIndex.return_value = 1
        main_window._stacked_layout = stacked_layout
        main_window.viewShow(1234)
        fill.assert_called_once_with(1234)
        assert main_window._history[0] == 1

    @patch('PyQt5.QtWidgets.QStackedLayout.setCurrentIndex')
    def test_on_back(sci, main_window):
        main_window._history = [1234]
        main_window.onBack()
        sci.assert_called_once_with(1234)

    @patch('podcastista.MainWindow.MainWindow.loadData')
    @patch('podcastista.MainWindow.MainWindow.clearData')
    def test_follow_show(load, clear, main_window):
        main_window._spotify = MagicMock()
        main_window.followShow(1234)
        load.assert_called_once()
        clear.assert_called_once()

    @patch('podcastista.MainWindow.MainWindow.loadData')
    @patch('podcastista.MainWindow.MainWindow.clearData')
    def test_unfollow_show(load, clear, main_window):
        main_window._spotify = MagicMock()
        main_window.unfollowShow(1234)
        load.assert_called_once()
        clear.assert_called_once()

    @patch('podcastista.EpisodeDetails.EpisodeDetails.fill')
    def test_view_episode(fill, main_window):
        stacked_layout = MagicMock()
        stacked_layout.currentIndex.return_value = 1
        main_window._stacked_layout = stacked_layout
        main_window.viewEpisode(1234)
        fill.assert_called_once_with(1234)

    @patch('podcastista.SearchTab.SearchTab.search')
    def test_on_search(search, main_window):
        stacked_layout = MagicMock()
        stacked_layout.currentIndex.return_value = 1
        main_window.onSearch()
        search.assert_called_once()

    @patch('podcastista.SearchTab.SearchTab.clear')
    def test_on_search_text_changed(clear, main_window):
        main_window.onSearchTextChanged("")
        clear.assert_called_once()

    def test_on_left_group_clicked(main_window):
        main_window.onLeftGroupClicked(main_window._left_listen_now)
        main_window.onLeftGroupClicked(main_window._left_shows)
        main_window.onLeftGroupClicked(main_window._left_latest_episodes)

    @patch('podcastista.MainWindow.MainWindow.reportUnknownDeviceId')
    def test_start_playback_unk(rep, main_window):
        spotify = MagicMock()
        main_window._spotify = spotify
        main_window.startPlayback(['uri1', 'uri2'])
        rep.assert_called_once()

    def test_start_playback(main_window):
        spotify = MagicMock()
        main_window._spotify = spotify
        main_window._player._active_device_id = 1234
        main_window.startPlayback(['uri1', 'uri2'])
        spotify.start_playback.assert_called_once()

    @patch('podcastista.MainWindow.MainWindow.reportUnknownDeviceId')
    def test_add_to_queue_unk(rep, main_window):
        spotify = MagicMock()
        main_window._spotify = spotify
        main_window.addToQueue(['uri1', 'uri2'])
        rep.assert_called_once()

    def test_add_to_queue(main_window):
        spotify = MagicMock()
        main_window._spotify = spotify
        main_window._player._active_device_id = 1234
        main_window.addToQueue(['uri1', 'uri2'])
        spotify.add_to_queue.assert_called_once()

    @patch('podcastista.LatestEpisodesListTab.LatestEpisodesListTab.fill')
    @patch('podcastista.MainWindow.MainWindow._restoreState')
    def test_on_shows_loaded(restore, fill, main_window):
        main_window.onShowsLoaded(['show1', 'show2'])
        restore.assert_called_once()
        fill.assert_called_once_with(['show1', 'show2'])

    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_show_notification(timer, main_window):
        main_window._notification = MagicMock()
        main_window.showNotification("text")
        timer.assert_called_once()

    def test_on_notification_fade_out(main_window):
        main_window.onNotificationFadeOut()
