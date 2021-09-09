
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
