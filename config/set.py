from .get import config_loc
import pytoml

def set_default(widget_name, default):
	'''Add a section for a widget to the config file with the config's defaults.'''
	with open(config_loc, 'a') as c:
		c.write('\n')
		c.write('[{}]\n'.format(widget_name))
		c.write(default.rstrip() + '\n')