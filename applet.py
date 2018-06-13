# from widgets.bostoncalendar.parse_calendar_stub import build_calendar_items
from menus.gtk.indicator import Indicator
from menus.xml_to_obj import parse
import xml.etree.ElementTree as ET

APPINDICATOR_ID = "bostoncalendar"

def main():
  indicator = Indicator()
  indicator.set_menu(build_menu_items())
  indicator.go()

def build_menu_items():
  widgets = [build_system_items]
  widgets_xml = [w() for w in widgets]
  menu_xml = ET.Element("menu-base")
  for w in widgets_xml:
    if w.__class__.__name__ == 'Element':
      menu_xml.append(w)
    elif w.__class__.__name__ == 'str':
      menu_xml.append(ET.fromstring(w))
    else:
      raise AppletError("Menu was given something besides an element or a str: {}".format(w.__class__.__name__))
  return parse(menu_xml)

def build_system_items():
  quit_button = ET.Element("item", {"action": "quit"})
  quit_button.text = "Quit"
  return quit_button

if __name__ == "__main__":
  main()

class AppletError(Exception):
  pass