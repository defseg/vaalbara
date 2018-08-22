# A base menu has:
#   - an items array of menus and items
#   - nothing else
#   - TODO: make this its own class?
# A `menu` has:
#   - an items array of menus and items
#   - text - the title of the menu
# A `MenuItem` has:
#   - a data dictionary, which may contain:
#     - an `action` key to determine what to do when the user clicks the item
#     - Existing actions are:
#       - navigate: open the value of `data['url']` in a web browser
#       - quit: quit
#     Presumably this will be expanded later.
#   - text - the title of the item

import xml.etree.ElementTree as ET

def parse(el):
  if el.tag == 'menu' or el.tag == 'menu-base':
    return _parse_menu(el)
  elif el.tag == 'item':
    return _parse_item(el)
  else:
    raise MenuParserError('Tag isn\'t menu or item: {}'.format(el.tag))

def _parse_menu(el):
  text = el.text or ''
  curr = Menu(text.strip())
  curr.add([parse(child) for child in el.findall('*')])
  return curr

def _parse_item(el):
  curr = MenuItem(el.text.strip(), el.attrib)
  return curr

class Menu:
  def __init__(self, text, items = None):
    self.text = text
    if items is None:
      self.items = []
    else:
      self.items = items
  def __repr__(self):
    return 'Menu: {}; items: {}'.format(self.text, len(self.items))
  def append(self, item):
    self.items.append(item)
  def add(self, new_items):
    self.items += new_items

class MenuItem:
  def __init__(self, text, data = {}):
    self.text = text
    action = data.pop('action', None)
    self.data = data
    self.action = action
  def __repr__(self):
    return 'MenuItem: {} - Data: {}'.format(self.text, self.data)

class MenuParserError(Exception):
  pass