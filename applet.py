from gi.repository import Gtk
from widgets.bostoncalendar.parse_calendar import build_calendar_items
from menu import append_all, init_menu

APPINDICATOR_ID = "bostoncalendar"

def main():
  indicator = init_menu()
  indicator.set_menu(build_menu())
  # Start GTK main loop
  Gtk.main()

def build_menu():
  menu = Gtk.Menu()
  append_all(menu, build_menu_items())
  menu.show_all()
  return menu

def build_menu_items():
  return build_calendar_items() + build_system_items()

def build_system_items():
  separator = Gtk.SeparatorMenuItem.new()
  item_quit = Gtk.MenuItem("Quit")
  item_quit.connect("activate", quit)
  return [separator, item_quit]

def quit(event_source):
  Gtk.main_quit()

if __name__ == "__main__":
  main()