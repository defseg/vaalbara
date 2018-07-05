# TODO need to figure out how to do refresh

from urllib2 import urlopen
import xml.etree.ElementTree as ET

def main(config):
	# TODO: OPML import
	return fetch_all(config['feeds'])

def fetch_all(feeds):
	menu = ET.Element('menu')
	menu.text = 'RSS'
	for feed in feeds:
		menu.append(parse(fetch(feed)))
	return menu

def fetch(feed):
	'''Open a feed's URL and ET the RSS.'''
	html = urlopen(feed).read()
	return ET.fromstring(html)

def parse(el):
	'''Parse an ElementTree `rss` element into XML for Vaalbara.'''
	menu = ET.Element('menu')
	menu.text = el.find('./channel/title').text
	for item in el.findall('./channel/item'):
		add_item(item, menu)
	return menu

def add_item(item, menu):
	'''Parse an ElementTree `item` element into XML for Vaalbara and append it to `menu`.'''
	item_el = ET.SubElement(menu, 'item')
	item_el.text             = item.find('title').text
	item_el.attrib['url']    = item.find('link').text
	item_el.attrib['action'] = 'navigate'