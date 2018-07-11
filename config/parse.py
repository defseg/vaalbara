from get import config_loc
import pytoml

# TODO: 
# - error checking
# - either replace pytoml or see about getting it to use an OrderedDict - order matters for e.g. RSS

def load_config():
	with open(config_loc) as f:
		config = pytoml.load(f)
	return config

config = load_config()