import requests
import string

from bs4 import BeautifulSoup

from soupselect import select

def furaffinity(thing, config):
	"""
	handler for furaffinity.net
	"""
	thing.url = string.replace(thing.url, 'view', 'full')

	page = requests.get(thing.url, cookies=config['cookies']).content

	soup = BeautifulSoup(page)

	image = soup.find(id="submissionImg")

	title = select(soup, '.cat b')[0].get_text()

	author = select(soup, '.cat a')[0].get_text()

	if image == None:
		return

	return {'link': 'http:' + image['src'], 'author': author, 'title': title}