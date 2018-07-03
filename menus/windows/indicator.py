from infi.systray import SysTrayIcon
from menu import build_menu_base

class Indicator:
	def __init__(self):
		self.menu_tuples = None

	def set_menu(self, menu_base):
		self.menu_tuples = build_menu_base(menu_base)

	def go(self):
		#                icon  hover_text
		with SysTrayIcon(None, 'Vaalbara', self.menu_tuples) as systray:
			pass