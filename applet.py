from config import config, set_default, load_text
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
  widget_list = [w for w in widget_list if w not in config['vaalbara'].get('disabled_widgets')]
  # Try to import all the widgets; skip anything that can't be imported
  def _import_widget(w):
    try:
      return importlib.import_module('widgets.{}'.format(w))
    except ImportError:
      print >> sys.stderr, 'Can\'t import widget {}\n'.format(w)
      return None
  # Can't have _import_widget return nothing at all, so filter out the Nones
  widgets = filter(None, (_import_widget(w) for w in widget_list))
  # Make sure each widget has a config; if one doesn't, try to load its default
  build_widget_configs(widgets, config)
  return widgets

def build_widget_configs(widgets, config):
  for widget in widgets:
    if _name(widget) not in config:
      if hasattr(widget, 'default'):
        set_default(_name(widget), widget.default)
        config[_name(widget)] = load_text(widget.default) # TODO maybe make this better
      else:
        set_default(_name(widget), '# No defaults given')


def build_menu_items(widgets):
  '''Call every loaded widget and concat them together into an XML description
  of the full menu to build. Widgets may return either an ElementTree element 
  or a string containing valid XML.
     Each widget has a `main` function, which receives one argument: the value
  in the `config` dict corresponding to the widget's name. For example, a 
  widget `foo` would receive `config['foo']` as an argument to its `main`.
  TODO: DTD'''
  widgets_xml = [w.main(config.get(_name(w))) for w in widgets]
  menu_xml = ET.Element('menu-base')
  for w in widgets_xml:
    if w.__class__.__name__ == 'Element':
      menu_xml.append(w)
    elif w.__class__.__name__ == 'str':
      menu_xml.append(ET.fromstring(w))
    else:
      raise AppletError('Menu was given something besides an element or a str: {}'.format(w.__class__.__name__))
  return parse(menu_xml)

def _name(widget):
  '''Get only the name of the widget, not the module path.'''
  return widget.__name__.split('.')[-1]

if __name__ == '__main__':
  main()

class AppletError(Exception):
  pass
