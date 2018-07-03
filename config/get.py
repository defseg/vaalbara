import os
from functools import reduce

def ensure_file(filename, defaults, *dirs):
    '''Ensure the existence of ~/{dir/dir/... in dirs}/filename.
    If it doesn't exist, initializes it with the contents of `defaults`.'''
    path = ensure_user_dirs(*dirs)
    file_loc = os.path.join(path, filename)
    if not os.path.isfile(file_loc):
        with open(file_loc, 'w') as f:
            f.write(defaults)
    return file_loc

def ensure_user_dirs(*dirs):
    '''For dirs = (foo, bar, baz), ensure existence of ~/foo, ~/foo/bar, ~foo/bar/baz.
    Then return the path ~/foo/bar/baz.'''
    def _ensure_dir(x, y):
        _path = os.path.join(x, y)
        if not os.path.isdir(_path):
            os.mkdir(_path)
        return _path
    return reduce(_ensure_dir, dirs, os.path.expanduser('~'))

config_filename = 'config.ini'
config_defaults = ''
config_path = ['.vaalbara']
config_loc = ensure_file(config_filename, config_defaults, *config_path)