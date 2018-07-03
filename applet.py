from config import config
import importlib, os, sys
from menus.indicator import Indicator
from menus.xml_to_obj import parse
import xml.etree.ElementTree as ET

def main():
  widgets = get_widgets(config)
  indicator = Indicator()
  indicator.set_menu(build_menu_items(widgets))
  indicator.go()

def get_widgets(config):
  '''Try to import every subdirectory of widgets/ except those listed in config['disabled_widgets'].'''
  # Get all subdirectories of widgets/
  # This is a little hairy, but it should work...
  here = os.path.split(os.path.abspath(sys.argv[0]))[0]
  widget_list = next(os.walk(os.path.join(here, 'widgets')))[1]
  # Filter out disabled widgets
  widget_list = [w for w in widget_list if w not in config['disabled_widgets']]
  # Try to import all the widgets; skip anything that can't be imported
  def _import_widget(w):
    try:
      return importlib.import_module('widgets.{}'.format(w))
    except ImportError:
      print >> sys.stderr, 'Can\'t import widget {}\n'.format(w)
      return None
  # Can't have _import_widget return nothing at all, so filter out the Nones
  return filter(None, (_import_widget(w) for w in widget_list))

def build_menu_items(widgets):
  '''Call every loaded widget and concat them together into an XML description
  of the full menu to build. Widgets may return either an ElementTree element 
  or a string containing valid XML.
  TODO: DTD'''
  widgets_xml = [w.main() for w in widgets]
  print ET.tostring(widgets_xml[0], encoding='utf8')
  menu_xml = ET.Element('menu-base')
  for w in widgets_xml:
    if w.__class__.__name__ == 'Element':
      menu_xml.append(w)
    elif w.__class__.__name__ == 'str':
      menu_xml.append(ET.fromstring(w))
    else:
      raise AppletError('Menu was given something besides an element or a str: {}'.format(w.__class__.__name__))
  return parse(menu_xml)

def build_system_items():
  quit_button = ET.Element('item', {'action': 'quit'})
  quit_button.text = 'Quit' 
  return quit_button

if __name__ == '__main__':
  main()

class AppletError(Exception):
  pass
