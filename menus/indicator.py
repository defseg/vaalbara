'''Import the Indicator module appropriate for the system.'''

import platform
system = platform.system()

if system == 'Windows':
	from windows.indicator import Indicator
elif system == 'Linux':
	from gtk.indicator import Indicator
else:
	raise IndicatorError('Unsupported OS: {}'.format(system))

class IndicatorError(Exception):
	pass