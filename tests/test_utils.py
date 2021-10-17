from podcastista import utils
import platform


def test_ms_to_time_mins():
    str = utils.msToTime(60000)
    assert str == '1 mins'


def test_ms_to_time_hours():
    str = utils.msToTime(60 * 60 * 1000 + 60000)
    assert str == '1h 1m'


def test_ms_to_play_time_mins():
    str = utils.msToPlayTime(60 * 1000 + 2000)
    assert str == '1:02'


def test_ms_to_play_time_hrs():
    str = utils.msToPlayTime(60 * 60 * 1000 + 60 * 1000 + 2000)
    assert str == '1:01:02'


def test_date_to_str():
    str = utils.dateToStr('2020-01-02')
    if platform.system() == 'Linux':
        assert str == "Thursday, 2 January 2020"
    else:
        assert str == "January 2, 2020"


def test_long_date():
    str = utils.longDate('2020-01-02')
    if platform.system() == 'Linux':
        assert str == "Thursday, 2 January 2020"
    else:
        assert str == "January 2, 2020"


def test_rating():
    assert utils.rating(True) == "Mature"
    assert utils.rating(False) == "Clean"
