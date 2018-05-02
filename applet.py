from gi.repository import Gtk
from gi.repository import AppIndicator3
from parse_calendar_stub import build_calendar_items
import signal

APPINDICATOR_ID = "bostoncalendar"

def main():
  indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID, "asdf", AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
  indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
  indicator.set_menu(build_menu())
  # Make it possible to ctrl+c
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  # Start GTK main loop
  Gtk.main()

def build_menu():
  menu = Gtk.Menu()
  for item in build_menu_items():
    menu.append(item)
  menu.show_all()
  return menu

def build_menu_items():
  return build_calendar_items() + build_system_items()

def build_system_items():
  item_quit = Gtk.MenuItem("Quit")
  item_quit.connect("activate", quit)
  return [item_quit]

def quit(event_source):
  Gtk.main_quit()

if __name__ == "__main__":
  main()