from PyQt5 import QtCore


def msToTime(ms):
    """ Convert milliseconds to human readable time"""
    secs = int(ms / 1000)
    mins = int(secs / 60)
    if mins < 60:
        return str(mins) + " mins"
    else:
        hrs = int(mins / 60)
        mins = int(mins % 60)
        return str(hrs) + "h " + str(mins) + "m"


def msToPlayTime(ms):
    """ Convert milliseconds to play time"""
    secs = int(ms / 1000)
    mins = int(secs / 60)
    if mins < 60:
        return "{}:{:02d}".format(mins, secs % 60)
    else:
        hrs = int(mins / 60)
        mins = int(mins % 60)
        return "{}:{:02d}:{:02d}".format(hrs, mins, secs % 60)


def dateToStr(date):
    qdate = QtCore.QDate.fromString(date, 'yyyy-MM-dd')
    locale = QtCore.QLocale.system()
    return locale.toString(qdate)


def longDate(date):
    qdate = QtCore.QDate.fromString(date, 'yyyy-MM-dd')
    locale = QtCore.QLocale.system()
    return locale.toString(qdate, locale.dateFormat())


def rating(explicit):
    if explicit:
        return "Mature"
    else:
        return "Clean"
