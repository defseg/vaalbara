from PySide import QtGui
from dispatcher import Dispatcher
from xml_to_obj import MenuItem
import sys

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = BaseMenu()
        self.setContextMenu(self.menu)

    def add_needed_items(self):
        quit_option = self.menu.addAction('Quit')
        quit_option.triggered.connect(QtGui.qApp.quit)

class BaseMenu(QtGui.QMenu):
    def __init__(self):
        QtGui.QMenu.__init__(self, "")
        self.widgets = {}

    def add_widget(self, menu):
        assert menu.__class__.__name__ == "Menu"
        self.widgets[menu.text] = QtMenu(menu, parent=self)
        self.addMenu(self.widgets[menu.text])

class QtMenu(QtGui.QMenu):
    def __init__(self, menu, parent=None):
        QtGui.QMenu.__init__(self, menu.text, parent)
        for i in menu.items:
            self.__add(i)

    def __add(self, thing):
        if thing.__class__.__name__ == "Menu":
            self.addMenu(QtMenu(thing, parent=self))
        elif thing.__class__.__name__ == "MenuItem":
            menu_item = self.addAction(thing.text)
            if thing.action:
                menu_item.triggered.connect(Dispatcher.get(thing))
        else:
            raise IndicatorError("{} isn't menu or item".format(thing))

class Indicator():
    def __init__(self):
        self.app     = QtGui.QApplication(sys.argv)
        icon_graphic = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DriveDVDIcon)
        self.icon    = SystemTrayIcon(icon_graphic)

    def set_menu(self, menu_base):
        for w in menu_base.items:
            self.icon.menu.add_widget(w)
        self.icon.add_needed_items()

    def go(self):
        self.icon.show()
        sys.exit(self.app.exec_())

class IndicatorError(Exception):
    pass