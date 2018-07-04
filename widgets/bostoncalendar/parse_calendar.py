# TODO test the caching stuff

from bs4 import BeautifulSoup, SoupStrainer, NavigableString
from urllib2 import urlopen
import xml.etree.ElementTree as ET
from bucket_schemas import boston_calendar_schema
import datetime

last_parsed_at = datetime.datetime.min
events = False

def build_calendar_items(config):
  # we don't do anything with the config yet
  if datetime.datetime.now().date() > last_parsed_at.date():
    set_events(fetch())
  return build_menu_contents()

def build_menu_contents():
  bucketing = boston_calendar_schema.bucketize(events)
  bucketing_keys = bucketing.keys()
  main_menu = ET.Element('menu')
  main_menu.text = 'Boston Calendar'
  for i in bucketing_keys:
    if bucketing[i]: # time block - contains array of dicts
      bucket = ET.SubElement(main_menu, 'menu')
      bucket.text = boston_calendar_schema.name(i)
      for item in bucketing[i]:
        item_text = item.pop('title')
        item_el = ET.SubElement(bucket, 'item', item)
        item_el.text = item_text
        item_el.attrib['action'] = 'navigate'
  return main_menu

def set_events(soup):
  global last_parsed_at, events
  last_parsed_at = datetime.datetime.now()
  events = parse(soup)

def fetch():
  html = urlopen('http://www.thebostoncalendar.com/').read()
  strainer = SoupStrainer('li', class_='event')
  return BeautifulSoup(html, parse_only=strainer)

def parse(soup):
  return [parse_one(li) for li in soup.find_all('li')]

def parse_one(li):
  title_el        = li.select_one('div.info > h3 > a')
  time_str_el     = li.select_one('p.time')
  location_el     = li.select_one('p.location')
  calendar_url_el = li.select_one('a[itemprop=url]')
  title        = title_el.contents[0]            if title_el        is not None else 'No title given'
  time_str     = parse_time(time_str_el)         if time_str_el     is not None else 'No time given'
  location     = location_el.contents[0].strip() if location_el     is not None else 'No location given'
  calendar_url = calendar_url_el.get('href')     if calendar_url_el is not None else 'No calendar URL given'
  return {'title': title, 'time': time_str, 'location': location, 'url': calendar_url}

def parse_time(time_str_el):
  return ''.join([c if isinstance(c, NavigableString) else parse_time(c.contents) for c in time_str_el]).strip()