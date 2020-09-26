from django.db import models
from ls.joyous.utils.telltime import timeFormat

def timeFormat(timeFormat):
    # e.g. 10:00am
    retval = ""
    if time_from != "" and time_from is not None:
        retval += prefix
        retval += dateformat.time_format(time_from, "f:s A").lower()
    if time_to != "" and time_to is not None:
        retval += infix
        retval += format(dateformat.time_format(time_to, "fA").lower())
    return retval.strip()
