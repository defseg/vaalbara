from get import config_loc
import pytoml

# TODO: error checking

def load_config():
	with open(config_loc) as f:
		config = pytoml.load(f)
	return config

config = load_config()