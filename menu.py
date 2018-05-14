from gi.repository import Gtk
from webbrowser import open as open_in_browser

def menuize(event):
  # Create a menu item from an event, and bind clicking on the event to
  # opening the event's Boston Calendar page.
  menu_item = Gtk.MenuItem(event.title)
  menu_item.connect("activate", navigate)
  menu_item.event_obj = event
  return menu_item

def navigate(e):
  if e.event_obj and e.event_obj.calendar_url:
    open_in_browser(e.event_obj.calendar_url)

def build_submenu(title, contents):
  # Build a submenu from a title and an array of MenuItems.
  submenu_item = Gtk.MenuItem(title)
  submenu = Gtk.Menu()
  submenu_item.set_submenu(submenu)
  append_all(submenu, contents)
  return submenu_item

def append_all(menu, contents):
  for item in contents:
    menu.append(item)
  return menu