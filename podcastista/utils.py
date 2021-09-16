from PyQt5 import QtCore


def msToTime(ms):
    """ Convert milliseconds to human readable time"""
    secs = int(ms / 1000)
    mins = int(secs / 60)
    if mins < 60:
        return str(int(ms / 1000 / 60)) + " mins"
    else:
        hrs = int(mins / 60)
        mins = int(mins % 60)
        return str(hrs) + "h " + str(mins) + "m"


def dateToStr(date):
    qdate = QtCore.QDate.fromString(date, 'yyyy-MM-dd')
    locale = QtCore.QLocale.system()
    return locale.toString(qdate)


def longDate(date):
    qdate = QtCore.QDate.fromString(date, 'yyyy-MM-dd')
    locale = QtCore.QLocale.system()
    return locale.toString(qdate, locale.dateFormat())
