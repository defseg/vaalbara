from gi.repository import Gtk, AppIndicator3
import menu as Menu
import signal

# kill GTK warning spew
import warnings
warnings.filterwarnings('ignore')

class Indicator:
  def __init__(self):
    ID       = 'Vaalbara'
    ICON     = 'todo'
    CATEGORY = AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
    self.indicator = AppIndicator3.Indicator.new(ID, ICON, CATEGORY)
    self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    # Make it possible to ctrl+c
    signal.signal(signal.SIGINT, signal.SIG_DFL)

  def go(self):
    Gtk.main()

  def set_menu(self, menu_base):
    self.indicator.set_menu(Menu.build_menu_base(menu_base))