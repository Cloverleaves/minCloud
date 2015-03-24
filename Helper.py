#!/usr/bin/python3
import math

class Helper(object):

    def def_date(time=False):
        """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
        from datetime import datetime
        now = datetime.now()
        if type(time) is int:
            diff = now - datetime.fromtimestamp(time)
        elif isinstance(time, datetime):
            diff = now - time
        elif not time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(second_diff) + " seconds ago"
            if second_diff < 120:
                return "a minute ago"
            if second_diff < 3600:
                return str(math.floor(second_diff / 60)) + " minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str(math.floor(second_diff / 3600)) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(day_diff) + " days ago"
        if day_diff < 31:
            return str(day_diff / 7) + " weeks ago"
        if day_diff < 365:
            return str(day_diff / 30) + " months ago"
        return str(day_diff / 365) + " years ago"

    def def_extension(extension):
        """Determine if particular icon is available."""
        icon = "undefined"
        if len(extension) == 2:
            ext = extension[1].lower()
            if ext in ['.txt', '.doc']:
                icon = "doc"
            elif ext in ['.bmp', '.eps', '.gif', '.jpg', '.jpeg', '.png', '.svg', '.tif', '.tiff']:
                icon = "image"
            elif ext in ['.flac', '.m3u', '.m4a', '.mid', '.mp3', '.mpa', '.ogg', '.wav', '.wma']:
                icon = "music"
            elif ext in ['.avi', '.flv', '.m4v', '.mov', '.mp4', '.mpg', '.swf', '.webm', '.wmv']:
                icon = "mov"
            elif ext in ['.7z', '.rar', '.tar.gz', '.zip']:
                icon = "archive"
            elif ext in ['.pdf']:
                icon = "pdf"

        return icon

    def sizeof_fmt(num, suffix='B'):
        """Return human readable size."""
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)
        