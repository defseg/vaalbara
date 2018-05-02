# We don't have caching yet, so stub out the stuff that hits any URLs.
from parse_calendar import CalendarEntry
from menu import menuize, build_submenu

events = []
events.append(CalendarEntry(title="Test item 1", time="Nowhen"   , location="Nowhere"   , calendar_url="https://www.example.com"))
events.append(CalendarEntry(title="Test item 2", time="Everywhen", location="Everywhere", calendar_url="https://www.asdf.com"))

def build_calendar_items():
  return [build_submenu("Boston Calendar", build_menu_contents())]

def build_menu_contents():
  return [menuize(event) for event in events]