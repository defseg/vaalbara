from gi.repository import Gtk, AppIndicator3

class MenuItem:
  def __init__(self, text, data = None, event = None):
    self.item = Gtk.MenuItem(text)
    self.data = data
    if event:
      self.bind(event)

  def bind(self, event):
    self.item.connect("activate", event)