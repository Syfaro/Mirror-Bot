import requests
import re


def e621(thing, config):
    """
    handler for e621.net
    """
    post_id = re.findall(r"e621.net/post/show/(\d+)", thing.url)

    if post_id is None:
        return None

    post_id = post_id[0]

    url = "https://e621.net/post/show/{}.json".format(post_id)

    post = requests.get(url).json()

    if '.swf' in post['file_url']:
        return None

    response = {'link': post['file_url']}

    if post['source'] != '':
        response['source'] = post['source']

    return response
