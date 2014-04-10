import requests
import re


def tumblr(thing, config):
    """
    Handler for tumblr
    """
    key = config['keys']['id']

    blog = thing.domain

    post_id = re.search(r"\d+", thing.url).group(0)

    api_url = '''http://api.tumblr.com/v2/blog/%s/posts/
                    photo?id=%s&api_key=%s''' % (blog, post_id, key)

    post = requests.get(api_url).json()

    img = len(post['response']['posts'][0]['photos'])

    if img == 1:

        response = {'link': post['response']['posts'][0]['photos'][0]\
                    ['alt_sizes'][0]['url'], 'source': thing.url,
                     'author': post['response']['blog']['name']}

        return response

    else:
        response = {'is_album': True, 'source': thing.url, 
                    'author': post['response']['blog']['name'], 'link': []}

        for l in range(img):

            response['link'].append(post['response']['posts'][0]\
                                        ['photos'][l]['alt_sizes'][0]['url'])

        return response