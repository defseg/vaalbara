from bs4 import BeautifulSoup, SoupStrainer, NavigableString
from urllib2 import urlopen
from collections import namedtuple
from menu import menuize, build_submenu
from bucket_schemas import boston_calendar_schema
import datetime

last_parsed_at = datetime.datetime.min
events = False

def build_calendar_items():
  if datetime.datetime.now().date() > last_parsed_at.date():
    set_events(fetch())
  return [build_submenu("Boston Calendar", build_menu_contents())]

def build_menu_contents():
  bucketing = boston_calendar_schema.bucketize(events)
  bucketing_keys = bucketing.keys()
  contents = []
  for i in bucketing_keys:
    if bucketing[i]:
      contents.append(build_submenu(boston_calendar_schema.name(i), [menuize(e) for e in bucketing[i]]))
  return contents

def set_events(soup):
  global last_parsed_at, events
  last_parsed_at = datetime.datetime.now()
  events = parse(soup)

def fetch():
  html = urlopen("http://www.thebostoncalendar.com/").read()
  strainer = SoupStrainer("li", class_="event")
  return BeautifulSoup(html, parse_only=strainer)

def parse(soup):
  return [parse_one(li) for li in soup.find_all("li")]

def parse_one(li):
  title_el        = li.select_one("div.info > h3 > a")
  time_str_el     = li.select_one("p.time")
  location_el     = li.select_one("p.location")
  calendar_url_el = li.select_one("a[itemprop=url]")
  title        = title_el.contents[0]            if title_el        is not None else "No title given"
  time_str     = parse_time(time_str_el)         if time_str_el     is not None else "No time given"
  location     = location_el.contents[0].strip() if location_el     is not None else "No location given"
  calendar_url = calendar_url_el.get("href")     if calendar_url_el is not None else "No calendar URL given"
  return CalendarEntry(title=title, time=time_str, location=location, calendar_url=calendar_url)

def parse_time(time_str_el):
  return "".join([c if isinstance(c, NavigableString) else parse_time(c.contents) for c in time_str_el]).strip()

CalendarEntry = namedtuple("CalendarEntry", ["title", "time", "location", "calendar_url"])