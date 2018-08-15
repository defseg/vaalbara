from webbrowser import open as open_in_browser
from PySide.QtGui import qApp

class Dispatcher:
    '''Dispatcher singleton so we can pass in methods from the applet without
    having to keep passing dictionaries into QtMenu.
    	The dispatcher is initialized with a dictionary of functions, to which
    some default functions are appended. All these functions take one argument:
    the menu item to which they're associated.'''
    __instance = None

    def __init__(self, funcs):
    	if Dispatcher.__instance == None:
    		Dispatcher.__instance = self
    		self.__funcs = {}
    		self.__funcs.update(funcs)
    		self.__funcs.update({
    			'navigate': _navigate,
    			'quit':     _quit
    		})

    @staticmethod 
    def get(obj):
        if obj.__class__.__name__ == 'str':
            return Dispatcher.__instance.__funcs[obj]
        return _curry(Dispatcher.__instance.__funcs[obj.action], obj)

def _curry(func, arg):
	return lambda *a, **b: func(arg, *a, **b)

def _navigate(obj):
	if obj.data and obj.data.get('url'):
		open_in_browser(obj.data['url'])

def _quit(obj):
	qApp.quit()