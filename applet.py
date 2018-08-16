from config import config, set_default, load_text
import importlib, os, sys
from menus.indicator import Indicator
from menus.dispatcher import Dispatcher
from menus.xml_to_obj import parse
import xml.etree.ElementTree as ET

def main():
  widgets = get_widgets(config)
  _print_loading_msg('All widgets loaded!')
  indicator = Indicator()
  build_dispatcher(widgets, indicator)
  indicator.set_menu(build_menu_items(widgets))
  _print_loading_msg('All menus built!')
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
      _print_loading_msg('Loading module {}'.format(w))
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

def build_dispatcher(widgets, indicator):
  defaults = {
    'refreshall': lambda: indicator.set_menu(build_menu_items(widgets))
  }

  for w in widgets:
    defaults['refresh_'+_name(w)] = lambda x: indicator.update_widget(parse(build_menu_item(w)))

  Dispatcher(defaults)

def build_menu_items(widgets):
  '''Call every loaded widget and concat them together into an XML description
  of the full menu to build. Widgets may return either an ElementTree element 
  or a string containing valid XML.
     Each widget has a `main` function, which receives one argument: the value
  in the `config` dict corresponding to the widget's name. For example, a 
  widget `foo` would receive `config['foo']` as an argument to its `main`.
  TODO: DTD'''
  menu_xml = ET.Element('menu-base')
  for w in widgets:
    menu_xml.append(build_menu_item(w))
  return parse(menu_xml)

def build_menu_item(widget):
  '''Call one loaded widget to get its menu, and return an ElementTree element
  containing the widget's menu.'''
  _print_loading_msg('Building menu for module {}'.format(_name(widget)))
  res = widget.main(config.get(_name(widget)))
  if res.__class__.__name__ == 'Element':
    pass
  elif w.__class__.__name__ == 'str':
    res = ET.fromstring(res)
  else:
    raise AppletError('Menu was given something besides an element or a str: {}'.format(w.__class__.__name__))
  # Append refresh option.
  refresh = ET.SubElement(res, 'item', {'action': 'refresh_'+_name(widget)})
  refresh.text = 'Refresh'
  return res

def _name(widget):
  '''Get only the name of the widget, not the module path.'''
  return widget.__name__.split('.')[-1]

def _print_loading_msg(text):
  '''Print some loading messages if display_loading_msgs is set to true in the 
  config.'''
  if config.get('vaalbara') and config.get('vaalbara').get('display_loading_msgs'):
    print text

if __name__ == '__main__':
  main()

class AppletError(Exception):
  pass
