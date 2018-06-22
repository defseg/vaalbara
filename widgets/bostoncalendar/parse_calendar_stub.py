# We don't have caching yet, so stub out the stuff that hits any URLs.
from bucket_schemas import boston_calendar_schema
import xml.etree.ElementTree as ET

_events = []
_events.append({'title':"Test item 1", "action":"navigate", "time":"Wednesday, May 02, 2018 07:00 A",          "location":"Nowhere"   , "url":"https://www.example.com"})
_events.append({'title':"Test item 2", "action":"navigate", "time":"Wednesday, May 02, 2018 07:00 P",          "location":"Everywhere", "url":"https://www.asdf.com"})
_events.append({'title':"Test item 3", "action":"navigate", "time":"Wednesday, May 02, 2018 goes until 05/03", "location":"Anywhere"  , "url":"https://en.wikipedia.org"})
_events.append({'title':"Test item 4", "action":"navigate", "time":"Wednesday, May 02, 2018 06:00 P",          "location":"Somewhere" , "url":"https://www.html5zombo.com"})

def build_menu_contents(events):
  bucketing = boston_calendar_schema.bucketize(events)
  bucketing_keys = bucketing.keys()
  main_menu = ET.Element('menu')
  main_menu.text = 'Boston Calendar'
  print bucketing
  for i in bucketing_keys:
    if bucketing[i]: # time block - contains array of dicts
      bucket = ET.SubElement(main_menu, 'menu')
      bucket.text = boston_calendar_schema.name(i)
      for item in bucketing[i]:
        print item
        item_text = item.pop('title')
        item_el = ET.SubElement(bucket, 'item', item)
        item_el.text = item_text
  return main_menu

def build_calendar_items():
  return build_menu_contents(_events)