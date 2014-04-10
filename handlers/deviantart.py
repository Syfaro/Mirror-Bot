import requests


def deviantart(thing, config):
	"""
	handler for deviantart.com
	"""
	api_url = "http://backend.deviantart.com/oembed?url={}".format(thing.url)

	post = requests.get(api_url).json()

	image = post['url']

	title = post['title']

	author = post['author_name']

	response = {'link': image, 'author': author,
				 'title': title, 'source': thing.url}

	return response