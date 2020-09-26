import datetime as dt
from datetime import timedelta
import calendar
from django import template
from wagtail.core.models import Site
from ls.joyous.utils.telltime import timeFormat, dateFormat
from ls.joyous.models.events import getAllEventsByDay
from ls.joyous.models.events import getAllUpcomingEvents
from ls.joyous.models.events import getGroupUpcomingEvents
from ls.joyous.models.events import getAllEventsByWeek
from ls.joyous.models.calendar import CalendarPage
from ls.joyous.utils.weeks import weekday_abbr, weekday_name
from ls.joyous.edit_handlers import MapFieldPanel

register = template.Library()

@register.inclusion_tag("joyous_additions/tags/event_highlights.html",
                        takes_context=True)
def event_highlights(context):
    # will be used when joyous is updated to later versions of django
    #request = Site.find_for_request(context['request'])
    #home = request.root_page
    request = context['request']
    home = request.site.root_page
    cal = CalendarPage.objects.live().descendant_of(home).first()
    calUrl = cal.get_url(request) if cal else None
    calName = cal.title if cal else None
    today = dt.date.today()
    tomorrow = today +timedelta(days=1)
    plus_two_days = today +timedelta(days=2)
    count_upcoming = len(getAllUpcomingEvents(request))
    if count_upcoming <= 12 and count_upcoming >= 3:
        num_days = 21
    elif count_upcoming < 3:
    	num_days = 31
    else:
        num_days = 8
    dateFrom = today
    dateTo   = today +timedelta(days=num_days)

    # we want 10 events to appear. If we iterate events and it's less than 10, than
    #we need to just grab the next 10 upcoming events without worrying about the range, or extend the dateTo range
    if cal:
        events = cal._getEventsByDay(request, dateFrom, dateTo)

    else:
        events = getAllEventsByDay(request, dateFrom, dateTo)
    return {'request':      request,
            'today':        today,
            'tomorrow':     tomorrow,
            'plus_two_days':    plus_two_days,
            'dateFrom':     dateFrom,
            'dateTo':     dateTo,
            'calendarUrl':  calUrl,
            'calendarName': calName,
            'events':       events }
