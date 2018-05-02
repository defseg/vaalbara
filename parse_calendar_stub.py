# We don't have caching yet, so stub out the stuff that hits any URLs.
from parse_calendar import CalendarEntry
from menu import menuize, build_submenu
from dateutil.parser import parse as parse_date

events = []
events.append(CalendarEntry(title="Test item 1", time="Wednesday, May 02, 2018 07:00 A"   , location="Nowhere"   , calendar_url="https://www.example.com"))
events.append(CalendarEntry(title="Test item 2", time="Wednesday, May 02, 2018 07:00 P", location="Everywhere", calendar_url="https://www.asdf.com"))
events.append(CalendarEntry(title="Test item 3", time="Wednesday, May 02, 2018 goes until 05/03", location="Everywhere", calendar_url="https://en.wikipedia.org"))

def build_calendar_items():
  return [build_submenu("Boston Calendar", build_menu_contents())]

def build_menu_contents():
  buckets = bucketize()
  buckets_keys = bucket_defs.keys()
  buckets_keys.sort()
  contents = []
  for i in buckets_keys:
    if buckets[i]:
      contents.append(build_submenu(bucket_defs[i], [menuize(e) for e in buckets[i]]))
  return contents

def initialize_buckets():
  d = {}
  for i in bucket_defs.keys():
    d[i] = []
  return d

def bucketize():
  buckets = initialize_buckets()
  for event in events:
    buckets[time_bucket(event)].append(event)
  return buckets

bucket_defs = {
  1: "Morning",
  2: "Afternoon",
  3: "Evening",
  4: "Night",
  8: "Multi-Day",
  9: "Unknown"
}

def time_bucket(entry):
  if "goes until" in entry.time:
    return 8
  try:
    hour = parse_date(entry.time).hour
  except:
    return 9
  if hour > 12:
    return 1
  elif hour > 17:
    return 2
  elif hour > 20:
    return 3
  else:
    return 4