from webbrowser import open as open_in_browser

def build_menu_base(obj):
  menu_base = tuple(_build(ch) for ch in obj.items)
  return menu_base

def _build(obj):
  obj_class = obj.__class__.__name__
  if obj_class == 'Menu':
    return (obj.text, None, tuple(_build(item) for item in obj.items))
  elif obj_class == 'MenuItem':
    return (obj.text, None, _dispatch_item_action(obj))
  else:
    raise MenuBuilderError("Wrong type: {}".format(obj_class))

def _dispatch_item_action(obj):
  dispatcher = {
    'navigate': _curry(_navigate, obj.data.get('url')),
    'quit': _do_nothing, # infi.systray handles appending a quit option - TODO move quit stuff to gtk from applet?
    None: None
  }
  return dispatcher[obj.action]

def _curry(func, arg):
  # TODO: is there a way to curry for named arguments instead of just positional ones?
  return lambda *a, **b: func(arg, *a, **b)

def _navigate(url, foo = None):
  if url:
    open_in_browser(url)

def _print(text):
  print text

def _do_nothing():
  pass

class MenuBuilderError(Exception):
  pass