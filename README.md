# vaalbara
Taskbar indicator menu multitool made of widgets. Not ready for release yet; consider the current version to be `-1.NaN.NaN`.

Uses Python 2.7, but may at some point be ported to 3.

# Dependencies
- `infi.systray` for Windows
- `gi` (PyGTKObject) for Linux (for now, you need support for `AppIndicator3`)

The one currently existing widget needs `python-dateutil` (dateutil) and `bs4` (BeautifulSoup).

# Writing widgets
Widgets must be directories containing an `__init__.py` that defines `main`. This `main` function must return an XML `menu` element.

Eventually there might be a DTD. For now:
- A `menu` contains text (the text to display) and `menu` or `item` elements.
- An `item` contains text and optional attributes:
  - An `action` attribute determines what to do on click. For now, the only implemented action is `navigate`, which opens the `item`'s `url` in a web browser.
