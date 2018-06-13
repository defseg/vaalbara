from webbrowser import open as open_in_browser
from gi.repository import Gtk

def build_menu_base(obj):
  menu_base = _build_and_append_all(obj)
  menu_base.show_all()
  return menu_base

def _build(obj):
  obj_class = obj.__class__.__name__
  if obj_class == 'Menu':
    return build_menu(obj)
  elif obj_class == 'MenuItem':
    return build_item(obj)
  else:
    raise GtkMenuBuilderError("Wrong type: {}".format(obj_class))

def build_menu(obj):
  menu = _build_and_append_all(obj)
  menu_item = Gtk.MenuItem(obj.text)
  menu_item.set_submenu(menu)
  return menu_item

def build_item(obj):
  item = Gtk.MenuItem(obj.text)
  if hasattr(obj, 'action'):
    item.connect('activate', _dispatch_item_action(obj))
  return item

def _build_and_append_all(obj):
  menu = Gtk.Menu()
  for i in obj.items:
    menu.append(_build(i))
  return menu

def _dispatch_item_action(obj):
  dispatcher = {
    'navigate': _curry(_navigate, obj.data.get('url')),
    'quit': Gtk.main_quit
  }
  return dispatcher[obj.action]

def _curry(func, arg):
  # TODO: is there a way to curry for named arguments instead of just positional ones?
  return lambda *a, **b: func(arg, *a, **b)

def _wrap(func, obj):
  # Gtk.MenuItem#connect sends an argument, so we need to get rid of it
  return func

def _navigate(url):
  if url:
    open_in_browser(url)

class GtkMenuBuilderError(Exception):
  pass